import distance
import numpy
import numpy as np
from PIL import Image
from PIL import ImageDraw


class Graph:
  def __init__(self, pic, annotations):
    self.nodes = []
    im = Image.open(pic)
    draw = ImageDraw.Draw(im)
    width, height = im.size

    for annotation in annotations:
      self.nodes.append(Node(draw, annotation))

    for node in self.nodes:
      node.adopt_children(self.nodes, draw, width, height)

    im.show()


class Node:
  def __init__(self, draw, annotation):
    self.description = annotation['description']
    self.vertices = annotation['boundingPoly']['vertices']
    xy = self.get_xys(self.vertices)
    draw.line(xy, fill=128)
    # self.center = numpy.array((int(np.mean([v[0] for v in xy])), int(np.mean([v[1] for v in xy]))))
    self.center = numpy.array([xy[0][0], xy[0][1]])
    self.children = []

  def adopt_children(self, nodes, draw, width, height):
    candidates = []
    for node in nodes:
      if node is self:
        continue
      if (self.center[0] - node.get_center()[0]) / width > .03 \
          or (self.center[1] - node.get_center()[1]) / height > .03:
        continue

      candidates.append((node, numpy.linalg.norm(self.center - node.center)))

    sorted_candidates = sorted(candidates, key=lambda x: x[1])
    self.children = list(map(lambda x: x[0], sorted_candidates[:2]))
    if draw:
      for child in self.children:
        draw.line(list(map(tuple, [self.center, child.get_center()])), fill=0)


        # o = min(enumerate(candidates), key=lambda x: numpy.linalg.norm(x[1].center, self.center))

  def get_center(self):
    return self.center


  def __repr__(self):
    s = "self: {}".format(self.description)
    for child in self.children:
      s = "{} child: {}".format(s, child.description)
    return s

  @staticmethod
  def get_xys(vertices):
    """
    :return: a list of (x,y) tuples: [(x,y),...]
    """
    return list((d['x'], d['y']) for d in vertices if 'x' in d and 'y' in d)
