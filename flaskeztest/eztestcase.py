"""EZTestCase class as well as its subclasses used be eztest package defined here."""

from unittest import TestCase

import flask
from selenium.common.exceptions import NoSuchElementException


class EZTestCase(TestCase):
    """Test cases that should be ran with flaskeztest 'eztest' command should inherit from this class."""
    FIXTURE = None

    def __init__(self, eztest, method_name='runTest'):
        TestCase.__init__(self, method_name)
        self.eztest = eztest
        self.driver = None
        self.fixture = self.__class__.FIXTURE
        self.eztestids = dict()

    def setUp(self):
        self.driver = self.eztest.driver
        self.eztest.reset_db()
        self.load_fixture()

    def navigate_to_endpoint(self, endpoint):
        with self.eztest.app.app_context():
            url = flask.url_for(endpoint, _external=True)
        self.driver.get(url)

    def load_fixture(self):
        self.eztestids = self.eztest.load_fixture(self.fixture)

    def assert_ele_exists(self, eztestid):
        try:
            self.driver.find_element_by_css_selector('*[%s="%s"]' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail_doesnt_exist(eztestid)

    def assert_ele_has_correct_text(self, eztestid):
        ele = self.get_ele(eztestid)
        self.assertEqual(ele.text.strip(), self.eztestids[eztestid],
                         self.get_incorrect_text_fail_mess(eztestid, ele.text.strip(), self.eztestids[eztestid]))

    def assert_full_model_exists(self, model):
        for eztestid in self.get_testids_for_model(model):
            self.assert_ele_exists(eztestid)

    def assert_full_fixture_exists(self):
        for eztestid in self.eztestids:
            self.assert_ele_exists(eztestid)

    def get_ele(self, eztestid):
        try:
            return self.driver.find_element_by_css_selector('*[%s="%s"]' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail_doesnt_exist(eztestid)

    # Helpers

    def get_testids_for_model(self, model):
        return [testid for testid in self.eztestids if testid.startswith(model) and
                testid[len(model)] in ('[', '.')]

    def fail_doesnt_exist(self, eztestid):
        self.fail("Element with eztestid=\"%s\" not found." % eztestid)

    @classmethod
    def get_incorrect_text_fail_mess(cls, eztestid, given_val, expected_val):
        return "Element with eztestid=\"%s\" has incorrect val. Expected=\"%s\", but Given=\"%s\"" \
               % (eztestid, expected_val, given_val)


class FullFixtureEZTestCase(EZTestCase):

    def __init__(self, eztest, fixture, endpoint, method_name='runTest'):
        EZTestCase.__init__(self, eztest, method_name)
        self.fixture = fixture
        self.endpoint = endpoint

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint)
        self.assert_full_fixture_exists()
