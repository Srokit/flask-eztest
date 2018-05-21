
from flaskeztest.eztestcase import EZTestCase


class TestCase1(EZTestCase):
    FIXTURE = 'simple'

    def setUp(self):
        self.load_fixture()
