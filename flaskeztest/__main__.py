"""Define functions which will be able to be ran through package."""

from importlib import import_module
import sys
import os

from helpers import parse_module_name_from_filepath

USAGE_MESSAGE = "Usage: eztest"


def flaskeztest_main(args=None):
    """
    Call this from main entry point of flaskeztest package.
    """

    flask_module = os.environ.get('FLASK_APP')

    flask_module = import_module(parse_module_name_from_filepath(flask_module))

    eztest = flask_module.eztest

    # Start up flask app and run our tests against it
    eztest.run()

    # To terminate the flask app thread started in eztest.run()
    sys.exit(0)


if __name__ == '__main__':
    flaskeztest_main()
