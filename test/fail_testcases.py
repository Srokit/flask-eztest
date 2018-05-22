
from flaskeztest import EZTestCase


class FailTC1(EZTestCase):
    FIXTURE = "twousers"

    def runTest(self):
        self.navigate_to_endpoint('index_two')
        self.assert_full_fixture_exists()
