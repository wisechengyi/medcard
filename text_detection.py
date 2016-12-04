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

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

SOURCE_DIR = 'sample_data'
RESULT_DIR = 'sample_result'

logging.basicConfig()

def main(photo_file):
  """Run a label request on a single image"""

  credentials = GoogleCredentials.get_application_default()
  service = discovery.build('vision', 'v1', credentials=credentials)

  src_path = os.path.join(SOURCE_DIR, photo_file)
  dest_path = os.path.join(RESULT_DIR, photo_file, '.json')

  if os.path.exists(dest_path):
    logging.info("{} already exists.".format(dest_path))
    with open(dest_path, 'rb') as f:
      logging.info(f.read())

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
    logging.info(response)
    with open(dest_path, 'wb') as f:
      f.write(json.dumps(response).encode())

      # label = response['responses'][0]['labelAnnotations'][0]['description']
      # print('Found label: %s for %s' % (label, photo_file))


if __name__ == '__main__':
  # parser = argparse.ArgumentParser()
  # parser.add_argument('image_file', help='The image you\'d like to label.')
  # args = parser.parse_args()
  main('1.jpg')
