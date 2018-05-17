"""EZTester class defined in this module."""

# Using phantomjs client so no browser will pop open during tests
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from flask import Flask
from subprocess import Popen
from os import getcwd

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy_seed import load_fixture_files, load_fixtures
import yaml

from exceptions import NotInitializedError
from eztesterclient import EZTesterClient


class EZTester(object):
    """
    A EZTester instance is the main component of the flaskeztest framework.
    Each asssertion method takes in the flask app that has the config dict that we will setup the tester object around.
    The SQL Alchemy object of the flask app should be already initialized by calling the init_app method of this object
    with the flask app passed into the EZTester constructor. Using this information the EZTester can prepare the rest of
    the flask app to render the page templates with testing attributes which the EZTester can check for via a selenium
    webdriver instance. The EZTester instance should be in some globally reachable module in your app so the tests and
    the templates can have access to its data. The EZTester instance will not inject its custom attributes into
    templates if flask_app.config['PY_ENV'] != 'test'.
    """

    DEFAULT_SELENIUM_WAIT_TIME = 1.5

    def __init__(self):
        object.__init__(self)
        self.initialized = False
        self.css_selector = '_eztestid'  # Default
        self.fixtures_dir = './fixtures'  # Default
        self.db_session = None
        self.eztestids = dict()
        self.flask_app = None
        self.flask_app_name = None
        self.flask_app_proc = None

    def init_app_and_db(self, flask_app, sqlalchemy_db):
        if not isinstance(flask_app, Flask):
            raise TypeError("flask_app argument to init_app_and_db must be a Flask app.")
        if not isinstance(sqlalchemy_db, SQLAlchemy):
            raise TypeError("sqlalchemy_db argument to init_app_and_db must be an SQLAlchemy instance.")
        if not flask_app.extensions.get('sqlalchemy'):
            sqlalchemy_db.init_app(flask_app)

        self.flask_app = flask_app

        with self.flask_app.app_context():
            self.db_session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=sqlalchemy_db.engine))

        if flask_app.config.get('EZTEST_FIXTURES_DIR'):
            self.fixtures_dir = flask_app.config.get('EZTEST_FIXTURES_DIR')
        if flask_app.config.get('EZTEST_CSS_SELECTOR'):
            self.css_selector = flask_app.config.get('EZTEST_CSS_SELECTOR')

        # else user should call reister_model_classes function for fixtures

        # TODO: Look at flask_app.config

        # TODO: Setup self.css_selector from config['EZTEST_CSS_SELECTOR'] key

        # TODO: Map seed data to eztestids by looking at sqlalchemy db schema

        self.initialized = True

    def get_client_after_loading_fixture(self, fixture_name, fix_dir=None):
        if not self.initialized:
            raise NotInitializedError()

        if fix_dir is None:
            fix_dir = self.fixtures_dir

        fixtures = load_fixture_files(fix_dir, [fixture_name+'.yaml'])
        load_fixtures(self.db_session, fixtures)

        with open('%s/%s.yaml' % (fix_dir, fixture_name)) as stream:
            models = yaml.load(stream)
        self.parse_eztestids_from_models(models)

        client = EZTesterClient(self.eztestids, self.css_selector)
        return client

    def assert_ele_exists(self, ele_id):
        try:
            self.sel_client.find_element_by_css_selector('[%s="%s"]' % (self.css_selector, ele_id))
        except NoSuchElementException:
            raise AssertionError("Did not find element with attribute %s=\"%s\"." % (self.css_selector, ele_id))

    # Private Helpers

    def startup_flask_app(self):
        self.flask_app_proc = Popen(['flask', 'run'], env={'FLASK_APP': self.flask_app_name, 'PY_ENV': 'test'})

    def kill_flask_app(self):
        self.flask_app_proc.kill()

    def parse_eztestids_from_models(self, models):
        for model in models:
            model_parts = model['model'].split('.')
            model_name = model_parts[len(model_parts) - 1]
            model_id = model['id']
            fields = model['fields']
            for (field_name, val) in fields.iteritems():
                self.eztestids['%s[%d].%s' % (model_name, model_id, field_name)] = str(val)

    def make_classes_for_reflected_tables(self):
        with self.flask_app.app_context():
            metadata = MetaData()
            metadata.reflect(self.sqlalchemy_db.engine)
            base = automap_base(metadata=metadata)
            base.prepare()
            return base.classes


