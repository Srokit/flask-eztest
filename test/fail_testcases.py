
from flaskeztest import EZTestCase


class FailTC1(EZTestCase):
    FIXTURE = "twousers"

    def runTest(self):
        self.navigate_to_endpoint('index_two')
        self.assert_full_fixture_exists()


class AssertEleExistsThatWasntLoadedByFixture(EZTestCase):
    FIXTURE = "oneuser"

    def runTest(self):
        self.navigate_to_endpoint('index_one')
        self.assert_ele_exists('User.lastname')


class AttemptToLoadAFixtureThatDoesntExist(EZTestCase):
    FIXTURE = "Invalid"

    def runTest(self):
        self.fail("should not get here")
