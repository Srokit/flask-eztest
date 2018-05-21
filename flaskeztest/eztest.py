
import threading
from unittest import TextTestRunner
import json

from selenium.webdriver.phantomjs.webdriver import WebDriver

from eztestcase import EZTestCase
from eztestsuite import EZTestSuite


class EZTest(object):
    """Primary object for flaskeztest package."""

    def __init__(self):
        self.app = None
        self.db = None
        self.driver = None
        self.testing = None
        self.model_clases = None

    def init_with_app_and_db(self, app, db):
        self.app = app
        self.db = db
        # For now assumer user called db.init_app(app)

        # Create dict with values being model class name and their values being the class itself
        model_class_objs = self.db.Model.__subclasses__()
        self.model_clases = dict([(obj, obj.__name__) for obj in model_class_objs])

        self.testing = self.app.config.get('PY_ENV') == 'test'

        # So eztestid function will work in all view function templates
        self.register_ctx_processor()

    def run(self):

        def run_app(app):
            app.run('127.0.0.1', port=5000)

        app_thread = threading.Thread(target=run_app, args=(self.app, ))
        app_thread.setDaemon(True)
        app_thread.start()

        test_case_classes = EZTestCase.__subclasses__()

        test_cases = [tc_class(self) for tc_class in test_case_classes]

        # For now package them all in the same suite
        suite = EZTestSuite(test_cases)

        runner = TextTestRunner()

        runner.run(suite)
        # Note when we come out of this function the main thread must call sys.exit(0) for flask app to stop running

    # These 2 are used by EZTestSuite before and after running tests

    def start_driver(self):
        self.driver = WebDriver()

    def quit_driver(self):
        self.driver.quit()

    # Used by EZTestSuite objects to load fixtures

    def load_fixture(self, fixture):
        """Seed DB with data in fixture json file and then return the testids also parsed from the file as dict."""

        models = self.parse_model_dicts_from_fixture(fixture)

        eztestids_for_fixture = dict()

        for (i, model) in enumerate(models):
            eztestids_for_fixture.update(**self.eztestids_from_model_dict(model, i))
            self.seed_db_with_model_dict(model)

        return eztestids_for_fixture

    # Private helpers

    def parse_model_dicts_from_fixture(self, fixture):

        # For now just make fixture dir the static
        return json.loads(open('./test/fixtures/%s' % (fixture+'.json')).read())

    def eztestids_from_model_dict(self, model, model_i):

        eztestids = dict()

        for (field, field_val) in model['fields'].iteritems():
            eztestids['%s[%d].%s' % (model['model'], model_i, field)] = str(field_val)

        return eztestids

    def seed_db_with_model_dict(self, model):
        self.db.session.add(self.model_clases[model['model']](**model['fields']))

    def register_ctx_processor(self):

        def eztestid_func(eztestid):
            if self.testing:
                return '_eztestid='+eztestid
            else:
                return ''

        def ctx_proc():
            return dict(_eztestid=eztestid_func)

        self.app.context_processor(ctx_proc)