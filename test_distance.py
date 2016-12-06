import json
import os
import unittest

from detection import get_distance_to_group, GROUP_RXBIN
from text_detection import compute_text, SOURCE_DIR, find_rxbin, RESULT_DIR


class TestStringMethods(unittest.TestCase):
  def test_upper(self):
    print(get_distance_to_group('rbine', GROUP_RXBIN))
    print(get_distance_to_group('ounitedhealthcare', GROUP_RXBIN))

  def test_rxbin(self):
    results = []
    for pic in sorted(os.listdir(RESULT_DIR), key=lambda x: int(x.split('.')[0])):
      with open(os.path.join(RESULT_DIR, pic), 'r') as f:
        response = json.load(f)
      # logger.info(pformat(response))
      all_fields = response['responses'][0]['textAnnotations'][0]['description'].lower().splitlines()
      results.append(find_rxbin(all_fields))
      # find_member_id(all_fields)
      # break

    self.assertEqual(['004336', '610014', None, '003585', '600428', '003858', '610014', '00000', '444444', '016499', '016580', '610014', '610241', '003858', '004336', '011867', None],
                     results)
