
from flaskeztest import RouteEZTestCase, expect_fixture


class IndexOneTestCase(RouteEZTestCase):
    FIXTURE = 'oneuser'

    def runTest(self):
        RouteEZTestCase.runTest(self)
        expectation = expect_fixture('oneuser')
        self.assert_expectation_correct(expectation)
