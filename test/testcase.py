
from flaskeztest.eztestcase import EZTestCase


class TestCase1(EZTestCase):
    FIXTURE = 'simple'

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.driver.get('http://localhost:5000/2')
        self.assert_ele_exists('Table1[0].name')
        self.assert_ele_has_correct_text('Table1[0].name')


class TestCase2(EZTestCase):
    FIXTURE = 'simple'

    def setUp(self):
        EZTestCase.setUp(self)

    def runTest(self):
        self.driver.get('http://localhost:5000/2')
        self.assert_ele_exists('Table1[0].name')
        self.assert_ele_has_correct_text('Table1[0].name')
