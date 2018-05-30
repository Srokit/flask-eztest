import threading
import warnings
from unittest import TextTestRunner
import json
import tempfile
import os
from importlib import import_module

from flask_sqlalchemy import SQLAlchemy

import capybara
import capybara.selenium.driver

from eztestcase import EZTestCase
from eztestsuite import EZTestSuite
from helpers import parse_module_name_from_filepath, convert_sql_table_to_sqlite_table
from exceptions import FixtureDoesNotExistError


class EZTest(object):
    """Primary object for flaskeztest package."""

    def __init__(self):
        self.app = None
        self.db = None
        self.driver = None
        self.model_clases = None
        self.reflecting_schema = None
        self.sqlite_db_file = None
        self.sqlite_db_fn = None
        self.testcase_module_paths = None
        self.fixtures_dir = None

    def init_with_app_and_db(self, app, db):
        self.app = app
        capybara.default_driver = "selenium"
        capybara.app = self.app
        capybara.ignore_hidden_elements = False
        self.db = db

        warnings.filterwarnings("ignore", message="Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead")

        if self.app.config.get('EZTEST_REFLECTION_DB_URI'):
            self.reflecting_schema = True
            reflection_db_uri = self.app.config.get('EZTEST_REFLECTION_DB_URI')
            self.app.config['SQLALCHEMY_DATABASE_URI'] = reflection_db_uri
            reflection_db = SQLAlchemy(self.app)
            with self.app.app_context():
                self.db.Model.metadata.reflect(reflection_db.engine)
            self.model_clases = self.db.Model.metadata.tables
            for (_, table) in self.model_clases.iteritems():
                convert_sql_table_to_sqlite_table(table)
        else:
            self.reflecting_schema = False
            # Create dict with values being model class name and their values being the class itself
            model_class_objs = self.db.Model.__subclasses__()
            self.model_clases = dict([(obj.__name__, obj) for obj in model_class_objs])

        self.sqlite_db_file, self.sqlite_db_fn = tempfile.mkstemp()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.sqlite_db_fn

        self.testcase_module_paths = self.app.config.get('EZTEST_TESTCASE_MODULE_PATHS') or list()
        self.fixtures_dir = self.app.config.get('EZTEST_FIXTURES_DIR')

        self.import_testcase_modules()

        # So that we can use url_for before the app starts
        self.app.config['SERVER_NAME'] = 'localhost:5000'

        self.db.init_app(self.app)

    def run(self):

        def run_app(app):
            from werkzeug.serving import run_simple
            run_simple('127.0.0.1', 5000, app)

        app_thread = threading.Thread(target=run_app, args=(self.app, ))
        app_thread.setDaemon(True)
        app_thread.start()

        test_case_classes = EZTestCase.__subclasses__()

        test_cases = [tc_class(self) for tc_class in test_case_classes]

        # For now package them all in the same suite
        suite = EZTestSuite(self, test_cases)

        runner = TextTestRunner()

        # Give app a second to setup

        runner.run(suite)
        # Note when we come out of this function the main thread must call sys.exit(0) for flask app to stop running

    # These 3 are used by EZTestSuite before and after running tests

    def remove_db_file(self):
        os.remove(self.sqlite_db_fn)

    # Used by EZTestSuite objects to load fixtures

    def load_fixture(self, fixture):
        """Seed DB with data in fixture json file and then return the testids also parsed from the file as dict."""

        models = self.parse_model_dicts_from_fixture(fixture)

        expected_models = dict()

        with self.app.app_context():
            for model in models:
                if 'row' in model:  # Otherwise we would find 'rows' key
                    expected_models[model['model']] = model['row']
                    self.seed_db_with_row_dict(model['model'], model['row'])
                else:
                    expected_models[model['model']] = list()
                    for row in enumerate(model['rows']):
                        expected_models[model['model']].append(row)
                        self.seed_db_with_row_dict(model['model'], row)
            self.db.session.commit()

        return expected_models

    # Used by EZTestCase objects to reset data in between test cases
    def reset_db(self):
        with self.app.app_context():
            self.db.drop_all()
            self.db.create_all()
    # Private helpers

    def parse_model_dicts_from_fixture(self, fixture):
        try:
            return json.loads(open('%s/%s' % (self.fixtures_dir, fixture+'.json')).read())
        except (OSError, IOError):
            raise FixtureDoesNotExistError(self.fixtures_dir, fixture+'.json')

    def import_testcase_modules(self):
        for mod_path in self.testcase_module_paths:
            import_module(parse_module_name_from_filepath(mod_path))

    def seed_db_with_row_dict(self, model_name, row):
        if self.reflecting_schema:
            model_tab = self.model_clases[model_name]
            q = model_tab.insert().values(**row)
            self.db.engine.execute(q)
        else:
            self.db.session.add(self.model_clases[model_name](**row))
