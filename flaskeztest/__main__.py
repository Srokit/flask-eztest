"""Define functions which will be able to be ran through package."""

from importlib import import_module
import sys
import os
import logging

from helpers import parse_module_name_from_filepath
from eztest import EZTest


def flaskeztest_main():
    """
    Call this from main entry point of flaskeztest package.
    """

    # Get rid of annoying output for every request
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    flask_module = os.environ.get('FLASK_APP')
    if flask_module is None:
        print "ERROR: FLASK_APP enviromnet variable must be set"
        sys.exit(1)

    try:
        flask_module = import_module(parse_module_name_from_filepath(flask_module))
    except ImportError:
        print "ERROR: Could not import flask module \"%s\"" % flask_module
        sys.exit(1)

    try:
        app = flask_module.app
        db = flask_module.db
    except AttributeError:
        print "ERROR: Could not find app or db attribute on flask module."
        sys.exit(1)

    eztest = EZTest()
    eztest.init_with_app_and_db(app, db)

    # Start up flask app and run our tests against it
    eztest.run()

    # To terminate the flask app thread started in eztest.run()
    sys.exit(0)


if __name__ == '__main__':
    flaskeztest_main()
