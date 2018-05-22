"""Define functions which will be able to be ran through package."""

from importlib import import_module
import sys
import os
import logging

from helpers import parse_module_name_from_filepath


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
        eztest = flask_module.eztest
    except AttributeError:
        print "ERROR: Could not find eztest object from attribute \"eztest\" on \"%s\" module" % flask_module
        sys.exit(1)

    # Start up flask app and run our tests against it
    eztest.run()

    # To terminate the flask app thread started in eztest.run()
    sys.exit(0)


if __name__ == '__main__':
    flaskeztest_main()
