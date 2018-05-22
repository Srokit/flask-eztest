
import threading
from unittest import TextTestRunner
import json
import tempfile
import os
from importlib import import_module
import warnings

import time

from selenium.webdriver.phantomjs.webdriver import WebDriver

from eztestcase import EZTestCase, FullFixtureEZTestCase
from eztestsuite import EZTestSuite
from helpers import parse_module_name_from_filepath
from exceptions import PyEnvNotTestError, FixtureDoesNotExistError


class EZTest(object):
    """Primary object for flaskeztest package."""

    def __init__(self):
        self.app = None
        self.db = None
        self.driver = None
        self.testing = None
        self.model_clases = None
        self.sqlite_db_file = None
        self.sqlite_db_fn = None
        self.testcase_module_paths = None
        self.fixtures_dir = None
        self.full_fix_test_case_instances = []

    def init_with_app_and_db(self, app, db):
        self.app = app
        self.db = db

        self.testing = self.app.config.get('PY_ENV') == 'test'

        # Don't want to run a production flask app under thies test settings
        if not self.testing:
            return

        # Unfortunately PhantomJS is no longer maintained but its still useful for this purpose
        warnings.filterwarnings("ignore", message="Selenium support for PhantomJS has been deprecated, please use "
                                                  "headless versions of Chrome or Firefox instead")

        self.sqlite_db_file, self.sqlite_db_fn = tempfile.mkstemp()
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.app.config.get('EZTEST_SQLITE_DB_URI')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.sqlite_db_fn

        self.testcase_module_paths = self.app.config.get('EZTEST_TESTCASE_MODULE_PATHS')
        self.fixtures_dir = self.app.config.get('EZTEST_FIXTURES_DIR')

        self.import_testcase_modules()

        # So that we can use url_for before the app starts
        self.app.config['SERVER_NAME'] = 'localhost:5000'

        self.db.init_app(self.app)

        # Create dict with values being model class name and their values being the class itself
        model_class_objs = self.db.Model.__subclasses__()
        self.model_clases = dict([(obj.__name__, obj) for obj in model_class_objs])

        # So eztestid function will work in all view function templates
        self.register_ctx_processor()

    def run(self):

        if not self.testing:
            raise PyEnvNotTestError()

        def run_app(app):
            from werkzeug.serving import run_simple
            run_simple('127.0.0.1', 5000, app)

        app_thread = threading.Thread(target=run_app, args=(self.app, ))
        app_thread.setDaemon(True)
        app_thread.start()

        test_case_classes = EZTestCase.__subclasses__()
        test_case_classes.remove(FullFixtureEZTestCase)

        test_cases = [tc_class(self) for tc_class in test_case_classes]
        # Add in test cases defined through route decorators
        test_cases.extend(self.full_fix_test_case_instances)

        # For now package them all in the same suite
        suite = EZTestSuite(self, test_cases)

        runner = TextTestRunner()

        # Give flask app arbitrary time to setup
        time.sleep(0.5)

        runner.run(suite)
        # Note when we come out of this function the main thread must call sys.exit(0) for flask app to stop running

    # Decorators used by flask app view functions
    def expect_full_fixture(self, fixture):

        def decorator(view_func):
            if self.testing:
                endpoint = view_func.__name__
                tc_inst = FullFixtureEZTestCase(self, fixture, endpoint)
                self.full_fix_test_case_instances.append(tc_inst)
            return view_func

        return decorator

    # These 3 are used by EZTestSuite before and after running tests

    def start_driver(self):
        self.driver = WebDriver()
        self.driver.implicitly_wait(1)

    def quit_driver(self):
        self.driver.quit()

    def remove_db_file(self):
        os.remove(self.sqlite_db_fn)

    # Used by EZTestSuite objects to load fixtures

    def load_fixture(self, fixture):
        """Seed DB with data in fixture json file and then return the testids also parsed from the file as dict."""

        models = self.parse_model_dicts_from_fixture(fixture)

        eztestids_for_fixture = dict()

        with self.app.app_context():
            for model in models:
                if 'row' in model:  # Otherwise we would find 'rows' key
                    eztestids_for_fixture.update(**self.eztestids_from_row_dict(model['model'], model['row']))
                    self.seed_db_with_row_dict(model['model'], model['row'])
                else:
                    for row_i, row in enumerate(model['rows']):
                        eztestids_for_fixture.update(**self.eztestids_from_row_dict(model['model'], row, row_i))
                        self.seed_db_with_row_dict(model['model'], row)
            self.db.session.commit()

        return eztestids_for_fixture

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

    @classmethod
    def eztestids_from_row_dict(cls, model_name, row, row_i=None):
        eztestids = dict()
        for (field, field_val) in row.iteritems():
            if row_i is None:
                eztestids['%s.%s' % (model_name, field)] = str(field_val)
            else:
                eztestids['%s[%d].%s' % (model_name, row_i, field)] = str(field_val)
        return eztestids

    def import_testcase_modules(self):
        for mod_path in self.testcase_module_paths:
            import_module(parse_module_name_from_filepath(mod_path))

    def seed_db_with_row_dict(self, model_name, row):
        self.db.session.add(self.model_clases[model_name](**row))

    def register_ctx_processor(self):

        def eztestid_func(eztestid, index=None):
            if self.testing:
                if index is None:
                    return '_eztestid="%s"' % eztestid
                eztestid = eztestid.split('.')
                eztestid[0] += '[%d]' % index
                eztestid = '.'.join(eztestid)
                return '_eztestid="%s"' % eztestid
            else:
                return ''

        def ctx_proc():
            return dict(_eztestid=eztestid_func)

        self.app.context_processor(ctx_proc)
