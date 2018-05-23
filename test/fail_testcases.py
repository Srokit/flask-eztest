
from flaskeztest import EZTestCase
from flaskeztest.exceptions import FixtureDoesNotExistError, EztestidNotInFixture


class FailTC1(EZTestCase):
    FIXTURE = "twousers"

    def runTest(self):
        self.navigate_to_endpoint('index_two')
        try:
            self.assert_full_fixture_exists()
            self.fail("Should have failed assert full fixture exists")
        except AssertionError:
            pass


class AssertEleExistsThatWasntLoadedByFixture(EZTestCase):
    FIXTURE = "oneuser"

    def runTest(self):
        self.navigate_to_endpoint('index_one')
        try:
            self.assert_ele_exists('User.lastname')
            self.fail("Should have raised User.lastname is not an eztestid in fixture")
        except EztestidNotInFixture:
            pass


class AttemptToLoadAFixtureThatDoesntExist(EZTestCase):
    FIXTURE = "Invalid"

    def setUp(self):
        pass

    def runTest(self):
        try:
            EZTestCase.setUp(self)
            self.fail("Should not have gotten passed load_fixture")
        except FixtureDoesNotExistError:
            pass
