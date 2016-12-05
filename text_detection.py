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

from correct import get_rx_bin_candidate

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
    logger.info("{} already exists.".format(dest_path))
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


if __name__ == '__main__':
  # parser = argparse.ArgumentParser()
  # parser.add_argument('image_file', help='The image you\'d like to label.')
  # args = parser.parse_args()
  for pic in os.listdir(SOURCE_DIR):
    # logger.info(pic)
    response = compute_text('5.jpg')
    # logger.info(pformat(response))
    all_fields = response['responses'][0]['textAnnotations'][0]['description'].lower().splitlines()
    print(all_fields)
    alphabet_only = [''.join(i for i in x if i.isalpha()) for x in all_fields]
    print(alphabet_only)
    idx, candidate = get_rx_bin_candidate(alphabet_only)
    origin = all_fields[idx]
    print("origin: {}".format(origin))
    numbers = ''.join(x for x in origin if x.isdigit())
    print("rx bin: {}".format(numbers))
    break

