"""Staring point for running flaskeztest cli test."""

from app import eztester, db, app
import unittest

runner = unittest.TextTestRunner()

class TestCase1(unittest.TestCase):

    def setUp(self):
        self.eztester = eztester
        self.eztester.init_app_and_db(app, db)
        self.eztestclient = self.eztester.get_client_after_loading_fixture('simple')
        self.eztestclient.startup_driver()

    def runTest(self):
        self.driver = self.eztestclient.get_driver()
        self.driver.get('http://localhost:5000/')
        print "Loaded page"

    def tearDown(self):
        self.eztestclient.quit_driver()


def run():
    """Run all test cases using EZTesterClient"""
    runner.run(unittest.makeSuite(TestCase1))

if __name__ == '__main__':
    run()
