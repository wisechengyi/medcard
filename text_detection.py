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

import distance

from detection import get_candidate, get_distance_to_group, GROUP_RXBIN, GROUP_ID

from pprint import pformat
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from graph import Graph

SOURCE_DIR = 'sample_data'
RESULT_DIR = 'sample_result'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def compute_text(photo_file):
  """Run a label request on a single image"""

  credentials = GoogleCredentials.get_application_default()
  service = discovery.build('vision', 'v1', credentials=credentials)

  src_path = get_src_path(photo_file)
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


def get_src_path(photo_file):
  return os.path.join(SOURCE_DIR, photo_file)


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

  if expected_type is int:
    for f in subfields[idx:]:
      try:
        expected_type(f)
        return f
      except ValueError:
        pass
    return None

  elif expected_type is str:
    dist_field = get_distance_to_group(cleaned, group)

    dist_max = -1
    # candidate = (field, value)
    candidate = None
    for i in range(len(subfields)):
      left = ' '.join(subfields[:i])
      right = ' '.join(subfields[i:])
      if not left or not right:
        continue

      dist_left = get_distance_to_group(left, group)
      dist_right = get_distance_to_group(right, group)

      if dist_left >= dist_field and dist_right >= dist_field:
        continue

      if abs(dist_left - dist_right) > dist_max:
        dist_max = abs(dist_left - dist_right)
        if dist_left > dist_right:
          candidate = (right, left)
        else:
          candidate = (left, right)

    if candidate:
      return expected_type(candidate[1])
    else:
      return None


def get_neighbor_value(all_fields, original, expected_type, exclude=[]):
  num_str = None
  for offset in [1, -1]:
    try:
      num_str = all_fields[all_fields.index(original) + offset]
      typed_numstr = expected_type(num_str)
      if typed_numstr in exclude:
        continue
    except (ValueError, IndexError):
      pass
    else:
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
    # print("rx bin: {}".format(number))
    rxbin = number
  else:
    # try to find the closest number
    rxbin = get_neighbor_value(fields, line_of_interest, int)
    # print("rxbin by proximity: {}".format(rxbin))

  return rxbin

  # break


def find_member_id(fields, graph, exclude=[]):
  alphabet_only = [''.join(i if i.isalpha() else ' ' for i in x).strip() for x in fields]
  idx, candidate = get_candidate(alphabet_only, GROUP_ID)
  if get_distance_to_group(candidate, GROUP_ID) >= 2:
    return None
  logger.debug("candidate: {}".format(candidate))
  line_of_interest = fields[idx]
  # print("origin: {}".format(line_of_interest))
  number = get_value(GROUP_ID, line_of_interest, str)
  if number:
    logger.debug("id: {}".format(number))
    member_id = number
  else:
    segment = graph.query(line_of_interest)
    if not segment:
      return None
    # try to find the closest number
    # member_id = get_neighbor_value(fields, line_of_interest, str, exclude=exclude)
    value_line = list(filter(lambda x: segment in x, fields))
    if len(value_line) != 1:
      return None
    member_id = value_line[0]
    logger.debug("id by proximity: {}".format(member_id))

  return member_id


if __name__ == '__main__':
  # parser = argparse.ArgumentParser()
  # parser.add_argument('image_file', help='The image you\'d like to label.')
  # args = parser.parse_args()
  ds_store = os.path.join(SOURCE_DIR, '.DS_Store')
  if os.path.exists(ds_store):
    os.remove(ds_store)
  for pic in sorted(os.listdir(SOURCE_DIR), key=lambda x: int(x.split('.')[0])):
    # if not ('jpg' in filename or 'png' in filename):
    #   continue
    # logger.info(pic)
    # pic = '16.png'
    response = compute_text(pic)
    # logger.info(pformat(response))
    all_fields = response['responses'][0]['textAnnotations'][0]['description'].lower().splitlines()
    try:
      g = Graph(get_src_path(pic), response['responses'][0]['textAnnotations'][1:])
    except ValueError as e:
      logger.error(e)
      continue

    rxbin = find_rxbin(all_fields)

    METHOD = distance.sorensen
    id = find_member_id(all_fields, g, exclude=[str(rxbin)])
    print("{}\t id: {}, rxbin: {}".format(pic, id, rxbin))

    # break
