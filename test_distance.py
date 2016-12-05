import unittest
from correct import get_distance_to_group, GROUP_RXBIN

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        print(get_distance_to_group('rbine', GROUP_RXBIN))
        print(get_distance_to_group('ounitedhealthcare', GROUP_RXBIN))