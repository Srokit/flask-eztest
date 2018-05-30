
from flaskeztest import EZTestCase
from flaskeztest.eztestsuite import EZTestSuite


class IndexTestCase(EZTestCase):

    FIXTURE = 'oneuser'

    def runTest(self):
        self.get_endpoint('index_one')
        self.assertTrue(self.does_field_exist('User', 'name'), "User name does not exist")


suite = EZTestSuite('index', __name__)
