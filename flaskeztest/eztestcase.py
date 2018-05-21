"""EZTestCase class defined here."""

from unittest import TestCase

from selenium.common.exceptions import NoSuchElementException


class EZTestCase(TestCase):
    """Test cases that should be ran with flaskeztest should inherit from this class."""
    FIXTURE = None

    def __init__(self, eztest, method_name='runTest'):
        TestCase.__init__(self, method_name)
        self.eztest = eztest
        self.driver = eztest.driver
        self.driver.implicitly_wait(1)
        self.fixture = self.__class__.FIXTURE
        self.eztestids = dict()

    def load_fixture(self):
        self.eztestids = self.eztest.load_fixture(self.fixure)

    def assert_ele_exists(self, eztestid):
        try:
            self.driver.find_elements_by_css_selector('*[@%s="%s"' % ('_eztestid', eztestid))
        except NoSuchElementException:
            self.fail('Did not find element')
