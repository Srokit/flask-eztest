"""EZTestCase class as well as its subclasses used be eztest package defined here."""

from unittest import TestCase

import capybara.dsl
import capybara


class EZTestCase(TestCase):
    """Test cases that should be ran with flaskeztest 'eztest' command should inherit from this class."""
    FIXTURE = None

    def __init__(self, eztest, method_name='runTest'):
        TestCase.__init__(self, method_name)
        self.eztest = eztest
        self.page = None
        self.driver = None
        self.base_url = 'http://localhost:5000'
        self.wait_time = 1  # Default
        self.fixture = self.__class__.FIXTURE
        self.expected_models = dict()

    def setUp(self):
        # self.driver = self.eztest.driver
        # self.driver.implicitly_wait(self.wait_time)
        self.page = capybara.dsl.page
        self.driver = self.page.driver.browser
        self.driver.implicitly_wait(self.wait_time)
        self.eztest.reset_db()
        self.load_fixture()

    def tearDown(self):
        capybara.reset_sessions()

    def navigate(self, path):
        self.page.visit(self.base_url + path)

    def load_fixture(self):
        self.expected_models = self.eztest.load_fixture(self.fixture)

    def assert_field_exists(self, model, field):
        assert type(self.expected_models[model]) is not list
        self.assertTrue(self.page.has_text(self.expected_models[model][field]))

    def assert_field_exists_with_row_index(self, model, index, field):
        assert type(self.expected_models[model]) is list
        self.assertTrue(self.page.has_text(self.expected_models[model][index][field]))

    def assert_field_is_visible(self, model, field):
        self.assert_field_exists(model, field)
        self.assertTrue(self.page.find('xpath', '*//*[text()="%s"]' % self.expected_models[model][field], visible="visible"))

    def assert_field_is_hidden(self, model, field):
        self.assert_field_exists(model, field)
        self.assertTrue(self.page.find('xpath', '*//*[text()="%s"]' % self.expected_models[model][field], visible="hidden"))

    def assert_table_with_fields_exists(self, model_fields, indices):
        for index in indices:
            for (model, field) in model_fields:
                self.assertTrue(self.page.find('xpath', '*//td[text()="%s"]' % (self.expected_models[model][index][field])))

    def assert_table_with_fields_hidden(self, model_fields, indices):
        for index in indices:
            for (model, field) in model_fields:
                self.assertTrue(self.page.find('xpath', '*//td[text()="%s"]' % (self.expected_models[model][index][field]), visible="hidden"))

    def assert_table_with_fields_visible(self, model_fields, indices):
        for index in indices:
            for (model, field) in model_fields:
                self.assertTrue(self.page.find('xpath', '*//td[text()="%s"]' % (self.expected_models[model][index][field]), visible="visible"))

    def get_element_for_field(self, model, field):
        self.assert_field_exists(model, field)
        self.page.find('xpath', '*//td[text()="%s"]' % (self.expected_models[model][field]))

    def get_element_for_field_with_row_index(self, model, index, field):
        self.assert_field_exists_with_row_index(model, index, field)
        self.page.find('xpath', '*//td[text()="%s"]' % (self.expected_models[model][index][field]))
