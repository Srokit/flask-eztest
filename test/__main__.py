"""Entry point to run tests."""

from unittest import TestCase, makeSuite, TextTestRunner
from flask_sqlalchemy import SQLAlchemy

from flaskeztest.eztester import EZTester
from app import app


class FlaskEZTestTesCase(TestCase):

    def setUp(self):
        self.flask_app = app
        self.sqlalchemy_db = SQLAlchemy()
        self.eztester = EZTester()

    def test_uninitialized(self):
        self.assertFalse(self.eztester.initialized)

    def test_initialization(self):
        self.eztester.init_app_and_db(self.flask_app, self.sqlalchemy_db)
        self.assertTrue(self.eztester.initialized)

if __name__ == '__main__':

    suite = makeSuite(FlaskEZTestTesCase)
    runner = TextTestRunner()

    runner.run(suite)
