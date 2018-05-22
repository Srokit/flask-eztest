
from unittest import TestSuite


class EZTestSuite(TestSuite):

    def __init__(self, eztest, tests):
        TestSuite.__init__(self, tests)
        self.eztest = eztest

    def run(self, result, debug=False):
        self.eztest.start_driver()
        TestSuite.run(self, result, debug)
        self.eztest.quit_driver()
        self.eztest.remove_db_file()
