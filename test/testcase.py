
from flaskeztest.eztestcase import EZTestCase


class TestCase1(EZTestCase):
    FIXTURE = 'simple'

    def setUp(self):
        EZTestCase.setUp(self)
        self.eztest.reset_db()
        self.load_fixture()
        print "After setup case 1"

    def runTest(self):
        self.driver.get('http://localhost:5000/')
        self.assert_ele_exists('Table1[0].name')
        self.assert_ele_has_correct_text('Table1[0].name')


class TestCase2(EZTestCase):
    FIXTURE = 'simple'

    def setUp(self):
        EZTestCase.setUp(self)
        self.eztest.reset_db()
        self.load_fixture()
        print "After setup case 2"

    def runTest(self):
        self.driver.get('http://localhost:5000/')
        self.assert_ele_exists('Table1[0].name')
        self.assert_ele_has_correct_text('Table1[0].name')
