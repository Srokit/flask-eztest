"""EzTestCase class defined here."""

from unittest import TestCase, TestSuite


class EZTestCase(TestCase):

    def __init__(self, method_name='runTest'):
        TestCase.__init__(self, method_name)


class EZTestSuite(TestSuite):

    def __init__(self, eztester, tests):
        TestSuite.__init__(self, tests)
        self.eztester = eztester

    def run(self):

        # TODO: Implement
        self.eztester.startup_driver()

        TestSuite.run(self, None)

        # TODO: Implement
        self.eztester.quite_driver()
