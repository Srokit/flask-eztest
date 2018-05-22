
from flaskeztest.eztestcase import EZTestCase


class TestCase1(EZTestCase):
    FIXTURE = 'twousers'

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.navigate_to_endpoint('index_two')
        self.assert_ele_exists('User[0].name')
        self.assert_ele_has_correct_text('User[0].name')


class TestCase2(EZTestCase):
    FIXTURE = 'twousers'

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.navigate_to_endpoint('index_two')
        self.assert_ele_exists('User[0].name')
        self.assert_ele_has_correct_text('User[0].name')
