"""
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Run the script on an image to get a label, E.g.:

    ./label.py <path-to-image>
"""

import base64
import json
import logging
import os

import itertools

from detection import get_candidate, get_distance_to_group, GROUP_RXBIN, GROUP_ID

from pprint import pformat
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

SOURCE_DIR = 'sample_data'
RESULT_DIR = 'sample_result'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def compute_text(photo_file):
  """Run a label request on a single image"""

  credentials = GoogleCredentials.get_application_default()
  service = discovery.build('vision', 'v1', credentials=credentials)

  src_path = os.path.join(SOURCE_DIR, photo_file)
  dest_path = os.path.join(RESULT_DIR, "{}.{}".format(photo_file, 'json'))

  if os.path.exists(dest_path):
    logger.debug("{} already exists.".format(dest_path))
    with open(dest_path, 'r') as f:
      response = json.load(f)
    return response

  with open(src_path, 'rb') as image:
    image_content = base64.b64encode(image.read())
    service_request = service.images().annotate(body={
      'requests': [{
        'image': {
          'content': image_content.decode('UTF-8')
        },
        'features': [{
          'type': 'TEXT_DETECTION',
          'maxResults': 1
        }]
      }]
    })
    response = service_request.execute()
    with open(dest_path, 'w') as f:
      f.write(json.dumps(response))
      return response

      # label = response['responses'][0]['labelAnnotations'][0]['description']
      # print('Found label: %s for %s' % (label, photo_file))


def get_value(group, original, expected_type):
  """
  Find the number given key and value are contained in the same original string.
  """
  cleaned = ''.join(c if c.isalnum() else ' ' for c in original)
  if all(c.isalpha() for c in cleaned):
    return None

  subfields = cleaned.split()
  if len(subfields) < 2:
    return None

  idx, field = min(enumerate(subfields), key=lambda x: get_distance_to_group(x[1], group))


  # dist_max = -1
  # candidate = None
  # for x, y in itertools.combinations(subfields, 2):
  #   dist_y = get_distance_to_group(y, group)
  #   dist_x = get_distance_to_group(x, group)
  #   if dist_y - dist_x > dist_max:
  #     dist_max = dist_y - dist_x
  #     candidate =

  for f in subfields[idx:]:
    try:
      expected_type(f)
      return f
    except ValueError:
      pass

  return None

def get_neighbor_number(all_fields, original):
  num_str = None
  for offset in [1, -1]:
    try:
      num_str = all_fields[all_fields.index(original) + offset]
      int(num_str)
    except (ValueError, IndexError):
      pass
    else:
      break
  else:
    return None

  return num_str


def find_rxbin(fields):
  # print(all_fields)
  alphabet_only = [''.join(i for i in x if i.isalpha()) for x in fields]
  # print(alphabet_only)
  idx, candidate = get_candidate(alphabet_only, GROUP_RXBIN)
  line_of_interest = fields[idx]
  # print("origin: {}".format(line_of_interest))
  numbers = ''.join(x for x in line_of_interest if x.isdigit())
  number = get_value(GROUP_RXBIN, line_of_interest, int)
  if number:
    print("rx bin: {}".format(number))
    rxbin = number
  else:
    # try to find the closest number
    rxbin = get_neighbor_number(fields, line_of_interest)
    print("rxbin by proximity: {}".format(rxbin))

  return rxbin

    # break

def find_member_id(fields):
  alphabet_only = [''.join(i if i.isalpha() else ' ' for i in x ).strip() for x in fields]
  idx, candidate = get_candidate(filter(lambda x: len(x) > 1, alphabet_only), GROUP_ID)
  print(candidate)
  line_of_interest = fields[idx]
  # print("origin: {}".format(line_of_interest))
  number = get_value(GROUP_ID, line_of_interest, str)
  if number:
    print("id: {}".format(number))
    rxbin = number
  else:
    # try to find the closest number
    rxbin = get_neighbor_number(fields, line_of_interest)
    print("id by proximity: {}".format(rxbin))

  return rxbin

if __name__ == '__main__':
  # parser = argparse.ArgumentParser()
  # parser.add_argument('image_file', help='The image you\'d like to label.')
  # args = parser.parse_args()
  for pic in sorted(os.listdir(SOURCE_DIR), key=lambda x: int(x.split('.')[0])):
    # logger.info(pic)
    # response = compute_text('12.png')
    # pic = '7.png'
    print(pic)
    response = compute_text(pic)
    # logger.info(pformat(response))
    all_fields = response['responses'][0]['textAnnotations'][0]['description'].lower().splitlines()
    # find_rxbin(all_fields)
    find_member_id(all_fields)
    # break
