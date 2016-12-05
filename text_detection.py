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

from correct import get_rx_bin_candidate, get_distance_to_group, GROUP_RXBIN

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


def get_number(group, original):
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
  for f in subfields[idx:]:
    try:
      int(f)
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



if __name__ == '__main__':
  # parser = argparse.ArgumentParser()
  # parser.add_argument('image_file', help='The image you\'d like to label.')
  # args = parser.parse_args()
  for pic in os.listdir(SOURCE_DIR):
    # logger.info(pic)
    # response = compute_text('12.png')
    # pic = '3.jpg'
    response = compute_text(pic)
    # logger.info(pformat(response))
    all_fields = response['responses'][0]['textAnnotations'][0]['description'].lower().splitlines()
    # print(all_fields)
    alphabet_only = [''.join(i for i in x if i.isalpha()) for x in all_fields]
    # print(alphabet_only)
    idx, candidate = get_rx_bin_candidate(alphabet_only)
    line_of_interest = all_fields[idx]
    # print("origin: {}".format(line_of_interest))
    numbers = ''.join(x for x in line_of_interest if x.isdigit())

    number = get_number(GROUP_RXBIN, line_of_interest)
    if number:
      print("{} rx bin: {}".format(pic, number))
    else:
      # try to find the closest number
      print("{} rxbin by proximity: {}".format(pic, get_neighbor_number(all_fields, line_of_interest)))

    # break

