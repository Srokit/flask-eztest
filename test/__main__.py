"""Entry point to run tests."""

from unittest import TestCase, makeSuite, TextTestRunner
from flask_sqlalchemy import SQLAlchemy

from flaskeztest.eztester import EZTester
from flaskeztest.__main__ import flaskeztest_main
from app import app

def runtests_explicitly():
    flaskeztest_main(['test/app.py', 'test/testmod.py'])

if __name__ == '__main__':

    runtests_explicitly()

    # suite = makeSuite(FlaskEZTestTesCase)
    # runner = TextTestRunner()
    #
    # runner.run(suite)
