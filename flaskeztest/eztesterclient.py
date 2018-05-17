"""Defines the EZTesterClient class;"""

from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from unittest import TestCase


class EZTesterClient(TestCase):

    DEFAULT_WAIT_TIME = 1.5

    def __init__(self, eztestids, css_selector, implicit_wait_time=DEFAULT_WAIT_TIME):
        TestCase.__init__(self)
        self.eztestids = eztestids
        self.css_selector = css_selector
        self.implicit_wait_time = implicit_wait_time
        self.driver = None

    def get_driver(self):
        """Used in cases where the user has a more fine grained use case for selenium."""
        return self.driver

    def startup_driver(self):
        self.driver = WebDriver()
        self.driver.implicitly_wait(self.implicit_wait_time)

    def quit_driver(self):
        self.driver.quit()

    # Assertion helpers for user

    def assert_exists(self, eztestid):
        try:
            self.driver.find_by_css_selector('[%s="%s"]' % (self.css_selector, eztestid))
        except NoSuchElementException:
            self.fail("Element with eztestid: \"%s\" not found")

    def assert_has_correct_val(self, eztestid):
        expected_val = self.eztestids[eztestid]
        try:
            ele = self.driver.find_by_css_selector('[%s="%s"]' % (self.css_selector, eztestid))
        except NoSuchElementException:
            self.fail("Element with eztestid: \"%s\" not found")
        self.assertEqual(ele.text.strip(), expected_val)