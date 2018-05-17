"""EZTester class defined in this module."""

# Using phantomjs client so no browser will pop open during tests
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from flask import Flask

from exceptions import NotInitializedError


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
        self.sel_client = None  # Will be instantiated in start_selenium_driver()
        self.css_selector = '_eztestid'  # Default

    def init_app(self, flask_app):
        if not isinstance(flask_app, Flask):
            raise TypeError("Argument to init_app must be a Flask app.")
        # TODO: Look at flask_app.config
        # TODO: Setup self.css_selector from ['EZTEST_CSS_SELECTOR'] key
        # TODO: Map seed data to eztestids by looking at sqlalchemy db schema
        self.initialized = True

    def start_selenium_driver(self):
        if not self.initialized:
            raise NotInitializedError()
        self.sel_client = WebDriver()
        self.sel_client.implicitly_wait(self.DEFAULT_SELENIUM_WAIT_TIME)

    def assert_ele_exists(self, ele_id):
        try:
            self.sel_client.find_element_by_css_selector('[%s="%s"]' % (self.css_selector, ele_id))
        except NoSuchElementException:
            raise AssertionError("Did not find element with attribute %s=\"%s\"." % (self.css_selector, ele_id))
