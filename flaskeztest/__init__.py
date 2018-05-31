"""The flaskeztest package"""

import capybara

# Passing imports along so user's can import commonly used objects from root package
from eztest import EZTest
from eztestcase import EZTestCase
from eztestsuite import EZTestSuite


@capybara.register_driver("selenium")
def init_selenium_driver(app):

    from capybara.selenium.driver import Driver

    return Driver(app, browser="phantomjs")