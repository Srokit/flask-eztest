"""EZTestCase class as well as its subclasses used be eztest package defined here."""

from unittest import TestCase

import flask
from selenium.common.exceptions import NoSuchElementException

from exceptions import EztestidNotInFixture


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
        if eztestid not in self.eztestids:
            raise EztestidNotInFixture(eztestid)
        try:
            self.driver.find_element_by_css_selector('*[%s="%s"]' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail_doesnt_exist(eztestid)

    def assert_ele_has_correct_text(self, eztestid):
        ele = self.get_ele(eztestid)
        self.assertEqual(ele.text.strip(), self.eztestids[eztestid],
                         self.get_incorrect_text_fail_mess(eztestid, ele.text.strip(), self.eztestids[eztestid]))

    def assert_full_model_exists(self, model, row_index=None, exclude_fields=[]):
        for eztestid in self.get_testids_for_model(model, row_index, exclude_fields):
            self.assert_ele_exists(eztestid)

    def assert_full_model_is_correct(self, model, row_index=None, exclude_fields=[]):
        for eztestid in self.get_testids_for_model(model, row_index, exclude_fields):
            self.assert_ele_has_correct_text(eztestid)

    def assert_full_fixture_exists(self, exclude_models=[], exclude_fields=[]):
        for eztestid in self.eztestids:
            field_name = self.field_name_from_eztestid(eztestid)
            model_name = self.model_name_from_eztestid(eztestid)

            if model_name not in exclude_models and ('%s.%s' % (model_name, field_name)) not in exclude_fields:
                self.assert_ele_exists(eztestid)

    def assert_full_fixture_is_correct(self, exclude_models=[], exclude_fields=[]):
        for eztestid in self.eztestids:
            field_name = self.field_name_from_eztestid(eztestid)
            model_name = self.model_name_from_eztestid(eztestid)

            if model_name not in exclude_models and ('%s.%s' % (model_name, field_name)) not in exclude_fields:
                self.assert_ele_has_correct_text(eztestid)

    def get_ele(self, eztestid):
        if eztestid not in self.eztestids:
            raise EztestidNotInFixture(eztestid)
        try:
            return self.driver.find_element_by_css_selector('*[%s="%s"]' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail_doesnt_exist(eztestid)

    # Helpers

    def get_testids_for_model(self, model, row_index=None, exclude_fields=[]):

        testids_to_return = []
        for testid in self.eztestids:
            field_name = self.field_name_from_eztestid(testid)
            if self.model_name_from_eztestid(testid) == model and field_name not in exclude_fields:
                if row_index is not None:
                    if self.row_index_from_eztestid(testid) == row_index:
                        testids_to_return.append(testid)
                else:
                    testids_to_return.append(testid)

        return testids_to_return

    def fail_doesnt_exist(self, eztestid):
        self.fail("Element with eztestid=\"%s\" not found." % eztestid)

    @classmethod
    def get_incorrect_text_fail_mess(cls, eztestid, given_val, expected_val):
        return "Element with eztestid=\"%s\" has incorrect val. Expected=\"%s\", but Given=\"%s\"" \
               % (eztestid, expected_val, given_val)

    @classmethod
    def field_name_from_eztestid(cls, eztestid):
            return eztestid[eztestid.index('.') + 1:]

    @classmethod
    def model_name_from_eztestid(cls, eztestid):
        if '[' in eztestid:
            return eztestid[:eztestid.index('[')]
        else:
            return eztestid[:eztestid.index('.')]

    @classmethod
    def row_index_from_eztestid(cls, eztestid):
        return int(eztestid[eztestid.index('[') + 1: eztestid.index(']')])


class ExpectFullFixtureEZTestCase(EZTestCase):

    def __init__(self, eztest, fixture, endpoint, exclude_models=[], exclude_fields=[], method_name='runTest'):
        EZTestCase.__init__(self, eztest, method_name)
        self.fixture = fixture
        self.endpoint = endpoint
        self.exclude_models = exclude_models
        self.exclude_fields = exclude_fields

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint)
        self.assert_full_fixture_is_correct(self.exclude_models, self.exclude_fields)


class ExpectModelTestCase(EZTestCase):

    def __init__(self, eztest, fixture, endpoint, model_name, row_index=None, exclude_fields=[], method_name='runTest'):
        EZTestCase.__init__(self, eztest, method_name)
        self.fixture = fixture
        self.endpoint = endpoint
        self.model_name = model_name
        self.row_index = row_index
        self.exclude_fields = exclude_fields

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint)
        self.assert_full_model_is_correct(self.model_name, self.row_index, self.exclude_fields)
