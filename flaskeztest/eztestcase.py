"""EZTestCase class defined here."""

from unittest import TestCase

from selenium.common.exceptions import NoSuchElementException


class EZTestCase(TestCase):
    """Test cases that should be ran with flaskeztest should inherit from this class."""
    FIXTURE = None

    def __init__(self, eztest, method_name='runTest'):
        TestCase.__init__(self, method_name)
        self.eztest = eztest
        self.driver = None
        self.fixture = self.__class__.FIXTURE
        self.eztestids = dict()

    def setUp(self):
        self.driver = self.eztest.driver

    def load_fixture(self):
        self.eztestids = self.eztest.load_fixture(self.fixture)

    def assert_ele_exists(self, eztestid):
        try:
            self.driver.find_element_by_css_selector('*[%s="%s"]' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail('Did not find element')

    def assert_ele_has_correct_text(self, eztestid):
        try:
            ele = self.driver.find_element_by_css_selector('*[%s="%s"]' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail('Did not find element')
        self.assertEqual(ele.text.strip(), self.eztestids[eztestid])
