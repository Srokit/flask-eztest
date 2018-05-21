"""Decorators for flaskeztest package defined here."""

from functools import wraps
from jinja2.exceptions import UndefinedError
from flask import Flask
from globals import eztest_globals


def eztest_route(f):
    """
    :type app: Flask
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        eztest_globals['app'].context_processor(f)
    return decorated_function
