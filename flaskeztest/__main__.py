"""Define functions which will be able to be ran through package."""

from subprocess import Popen, call
from sys import argv, exit
import os

USAGE_MESSAGE = "Usage: eztest flask_app_module_name"


def flaskeztest_main(args=None):
    """
    Call this from main entry point of flaskeztest package.

    args: ( flask_module_name [, test_module])
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
    env = os.environ
    env.update(FLASK_APP=flask_app_module, PY_ENV='test')
    flask_proc = Popen(['python', flask_app_module], env=env)

    print "Running test module %s" % test_module
    try:
        call(['python', test_module], env=env)
    except OSError as e:
        print "Problem running test:"
        print str(e)

    flask_proc.kill()
    print "Killed flask app"


if __name__ == '__main__':
    flaskeztest_main()
