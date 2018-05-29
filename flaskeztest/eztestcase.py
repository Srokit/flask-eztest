"""EZTestCase class as well as its subclasses used be eztest package defined here."""

from unittest import TestCase

import flask
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions import EztestidNotInFixture
from expectation import FixtureExpectation, ModelExpectation


class EZTestCase(TestCase):
    """Test cases that should be ran with flaskeztest 'eztest' command should inherit from this class."""
    FIXTURE = None

    def __init__(self, eztest, method_name='runTest'):
        TestCase.__init__(self, method_name)
        self.eztest = eztest
        self.driver = None
        self.wait_time = 1  # Default
        self.fixture = self.__class__.FIXTURE
        self.eztestids = dict()

    def setUp(self):
        self.driver = self.eztest.driver
        self.driver.implicitly_wait(self.wait_time)
        self.eztest.reset_db()
        self.load_fixture()

    def navigate_to_endpoint(self, endpoint, endpoint_kwargs=dict()):
        with self.eztest.app.app_context():
            url = flask.url_for(endpoint, _external=True, **endpoint_kwargs)
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

    def assert_ele_is_visible(self, eztestid):
        ele = self.get_ele(eztestid)
        try:
            WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of(ele)
            )
        except TimeoutException:
            self.fail("Element with eztestid=\"%s\" is not visible." % eztestid)

    def assert_ele_is_invisible(self, eztestid):
        ele = self.get_ele(eztestid)
        try:
            WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of(ele)
            )
            self.fail("Element with eztestid=\"%s\" is not hidden." % eztestid)
        except TimeoutException:
            pass

    def assert_full_model_exists(self, model, row_index=None, exclude_fields=[]):
        for eztestid in self.get_testids_for_model(model, row_index, exclude_fields):
            self.assert_ele_exists(eztestid)

    def assert_full_model_is_correct(self, model, row_index=None, exclude_fields=[]):
        for eztestid in self.get_testids_for_model(model, row_index, exclude_fields):
            self.assert_ele_has_correct_text(eztestid)

    def assert_model_field_is_correct(self, model, field, row_index=None):
        eztestids = [eztestid for eztestid in self.get_testids_for_model(model, row_index)
                     if self.field_name_from_eztestid(eztestid) == field]
        for testid in eztestids:
            self.assert_ele_has_correct_text(testid)

    def assert_model_field_is_visible(self, model, field, row_index=None):
        eztestids = [eztestid for eztestid in self.get_testids_for_model(model, row_index)
                     if self.field_name_from_eztestid(eztestid) == field]
        for testid in eztestids:
            self.assert_ele_is_visible(testid)

    def assert_model_field_is_invisible(self, model, field, row_index=None):
        eztestids = [eztestid for eztestid in self.get_testids_for_model(model, row_index)
                     if self.field_name_from_eztestid(eztestid) == field]
        for testid in eztestids:
            self.assert_ele_is_invisible(testid)

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

    def assert_expectation_correct(self, expectation):
        if expectation.expecting_all_models:
            self.assert_full_fixture_is_correct()
        elif expectation.expecting_specific_models:
            for model_exp in expectation.expected_models:
                assert isinstance(model_exp, ModelExpectation)
                if model_exp.expecting_all_fields:
                    self.assert_full_model_is_correct(model_exp.name, model_exp.index)
                elif model_exp.expecting_specific_fields:
                    for field_exp in model_exp.expected_fields:
                        self.assert_model_field_is_correct(model_exp.name, field_exp.name, model_exp.index)
                        if field_exp.check_visible:
                            self.assert_model_field_is_visible(model_exp.name, field_exp.name, model_exp.index)
                        elif field_exp.check_invisible:
                            self.assert_model_field_is_invisible(model_exp.name, field_exp.name, model_exp.index)
                else:
                    self.assert_full_model_is_correct(model_exp.name, exclude_fields=model_exp.unexpected_fields)
        else:  # self.fix_expectation_obj.not_expecting_specific_models == True
            self.assert_full_fixture_is_correct(exclude_models=expectation.unexpected_models)

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
        if len(testids_to_return) == 0:
            if row_index is not None:
                err_msg = "No eztestids found for model=\"%s\" at row_index=\"%d\"." % (model, row_index)
            else:
                err_msg = "No eztestids found for model=\"%s\"." % model
            self.fail(err_msg)
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
        try:
            return int(eztestid[eztestid.index('[') + 1: eztestid.index(']')])
        except IndexError:
            return None


class ExpectFullFixtureEZTestCase(EZTestCase):

    def __init__(self, eztest, fixture, endpoint, endpoint_kwargs=dict(), exclude_models=[], exclude_fields=[], method_name='runTest'):
        EZTestCase.__init__(self, eztest, method_name)
        self.fixture = fixture
        self.endpoint = endpoint
        self.endpoint_kwargs = endpoint_kwargs
        self.exclude_models = exclude_models
        self.exclude_fields = exclude_fields

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint, self.endpoint_kwargs)
        self.assert_full_fixture_is_correct(self.exclude_models, self.exclude_fields)


class ExpectModelTestCase(EZTestCase):

    def __init__(self, eztest, fixture, model_name, endpoint, endpoint_kwargs=dict(), row_index=None, exclude_fields=[], method_name='runTest'):
        EZTestCase.__init__(self, eztest, method_name)
        self.fixture = fixture
        self.endpoint = endpoint
        self.endpoint_kwargs = endpoint_kwargs
        self.model_name = model_name
        self.row_index = row_index
        self.exclude_fields = exclude_fields

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint, self.endpoint_kwargs)
        self.assert_full_model_is_correct(self.model_name, self.row_index, self.exclude_fields)


class ExpectTestCase(EZTestCase):

    def __init__(self, eztest, fix_expectation_obj, endpoint, endpoint_kwargs=dict()):
        EZTestCase.__init__(self, eztest)
        assert isinstance(fix_expectation_obj, FixtureExpectation)
        self.fix_expectation_obj = fix_expectation_obj
        self.fixture = self.fix_expectation_obj.name
        self.endpoint = endpoint
        self.endpoint_kwargs = endpoint_kwargs

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint, self.endpoint_kwargs)
        self.assert_expectation_correct(self.fix_expectation_obj)


class RouteEZTestCase(EZTestCase):

    def __init__(self, eztest, endpoint, endpoint_kwargs=dict()):
        EZTestCase.__init__(self, eztest)
        self.endpoint = endpoint
        self.endpoint_kwargs = endpoint_kwargs

    def runTest(self):
        self.navigate_to_endpoint(self.endpoint, self.endpoint_kwargs)
