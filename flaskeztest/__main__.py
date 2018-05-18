"""Define functions which will be able to be ran through package."""

from subprocess import Popen, call
from sys import argv, exit, path
import os
import threading
import unittest
import time

from importlib import import_module

print path

USAGE_MESSAGE = "Usage: eztest flask_app_module_name"

def flaskeztest_main(args=None):
    """
    Call this from main entry point of flaskeztest package.

    args: ( flask_module [, test_module])
    """
    if args is None:
        try:
            args = argv[1:]
        except IndexError:
            args = []

    if len(args) < 1 or len(args) > 2:
        print USAGE_MESSAGE
        exit(1)

    flask_app_module = args[0]

    if len(args) == 2:
        test_module = args[1]
    else:
        test_module = 'test'

    print "Starting flask app"

    print flask_app_module

    flask_mod = import_module(flask_app_module)
    app = flask_mod.app

    app_thread = threading.Thread(target=app.run, kwargs=dict(self=app, host='127.0.0.1', port=5000))
    app_thread.setDaemon(True)  # exiting will also end this thread
    app_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "exiting"
    exit()


if __name__ == '__main__':
    flaskeztest_main()
