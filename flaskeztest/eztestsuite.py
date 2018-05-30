
from unittest import TestSuite


class EZTestSuite(TestSuite):

    def __init__(self, eztest, tests):
        TestSuite.__init__(self, tests)
        self.eztest = eztest

    def run(self, result, debug=False):
        TestSuite.run(self, result, debug)
        self.eztest.remove_db_file()
