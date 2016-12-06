import distance

GROUP_RXBIN = {'rxbin', 'rx_bin', 'rx bin', 'bin', 'bin#'}
GROUP_RXGRP = {'rxgrp', 'rx group', 'rx_grp', 'rxgroup'}
GROUP_ID = {'enrollee id', 'member id', 'id', 'id number', 'identification #', 'member id #', 'member id number'}
GROUP_PCN = {'pcn'}

def get_distance_to_group(word, group):
  min_distance = min(distance.sorensen(word, x) for x in group)
  # print(word, min_distance)
  return min_distance


def get_rx_bin_candidate(field_list):
  """
  Find (idx, word) tuple out of the field list that is the best candidate for RxBin.
  """
  o = min(enumerate(field_list), key=lambda x: get_distance_to_group(x[1], GROUP_RXBIN))
  # print("o: {}".format(o))
  return o