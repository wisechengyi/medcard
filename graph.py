import distance
import numpy
import numpy as np
from PIL import Image
from PIL import ImageDraw
from scipy.spatial.distance import pdist, cdist


class Graph:
  def __init__(self, pic, annotations):
    self.nodes = []
    im = Image.open(pic)
    draw = ImageDraw.Draw(im)
    width, height = im.size

    if height < 300 or width < 400:
      raise ValueError("{} does not have enough resolution".format(pic))

    for annotation in annotations:
      self.nodes.append(Node(draw, annotation))

    for node in self.nodes:
      node.adopt_children(self.nodes, draw, width, height)

    # im.show()
    im.close()

  def query(self, keyword):
    for n in self.nodes:
      child = n.get_separated_child(keyword)
      if child:
        return child.get_description()
    else:
      return None

class Node:
  def __init__(self, draw, annotation):
    self.description = annotation['description'].lower()
    self.vertices = annotation['boundingPoly']['vertices']
    xy = self.get_xys()
    draw.line(xy, fill=128, width=2)
    # self.center = numpy.array((int(np.mean([v[0] for v in xy])), int(np.mean([v[1] for v in xy]))))
    self.center = numpy.array([xy[0][0], xy[0][1]])
    self.children = []

  def adopt_children(self, nodes, draw, width, height):
    candidates = []
    for node in nodes:
      if node is self:
        continue
      if (self.center[0] - node.get_center()[0]) / width > .1 \
          or (self.center[1] - node.get_center()[1]) / height > .1:
        continue


      candidates.append((node, self.get_min_distance(node)))

    sorted_candidates = sorted(candidates, key=lambda x: x[1])
    self.children = list(map(lambda x: x[0], sorted_candidates[:2]))
    if draw:
      for child in self.children:
        draw.line(list(map(tuple, [self.center, child.get_center()])), fill=0, width=3)

  def get_min_distance(self, other_node):
    m = cdist(self.get_xys(), other_node.get_xys(), p=2)
    return m.min()

  def get_center(self):
    return self.center

  def get_description(self):
    return self.description

  def __repr__(self):
    s = "self: {}".format(self.description)
    for child in self.children:
      s = "{} child: {}".format(s, child.description)
    return s

  def get_separated_child(self, keyword):
    for child in self.children:
      if self.description in keyword and child.get_description() in keyword:
        the_other_child = list(filter(lambda x: x is not child, self.children))
        if the_other_child:
          return the_other_child[0]


  def get_xys(self):
    """
    :return: a list of (x,y) tuples: [(x,y),...]
    """
    return list((d['x'], d['y']) for d in self.vertices if 'x' in d and 'y' in d)
