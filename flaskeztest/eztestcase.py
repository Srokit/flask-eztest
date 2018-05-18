"""EzTestCase class defined here."""

from unittest import TestCase


class EZTestCase(TestCase):

    def __init__(self, method_name='runTest'):
        TestCase.__init__(self, method_name)

