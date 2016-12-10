from functools import reduce
import numpy as np
from PIL import Image
from PIL import ImageDraw


class Graph:
  def __init__(self, pic, annotations):
    self.nodes = []
    im = Image.open(pic)
    draw = ImageDraw.Draw(im)

    for annotation in annotations:
      self.nodes.append(Node(draw, annotation))

    im.show()


class Node:
  def __init__(self, draw, annotation):
    self.description = annotation['description']
    self.vertices = annotation['boundingPoly']['vertices']
    xy= self.get_xys(self.vertices)
    draw.line(xy, fill=128)
    self.center = (np.mean([v[1] for v in xy]), np.mean([v[0] for v in xy]))

  @staticmethod
  def get_xys(vertices):
    """
    :return: a list of (x,y) tuples: [(x,y),...]
    """
    return list((d['x'], d['y']) for d in vertices if 'x' in d and 'y' in d)