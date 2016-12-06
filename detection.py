import distance

GROUP_RXBIN = {'rxbin', 'rx_bin', 'rx bin', 'bin', 'bin#'}
GROUP_RXGRP = {'rxgrp', 'rx group', 'rx_grp', 'rxgroup'}
GROUP_ID = {'enrollee id', 'member id', 'id', 'id number', 'identification', 'member id #', 'member id number',
            'subscriber id'}
GROUP_PCN = {'pcn'}


def get_distance_to_group(word, group):
  if not word:
    return 9999
  min_distance = min(distance.levenshtein(word, x) for x in group)
  # print(word, min_distance)
  return min_distance


def get_candidate(field_list, group):
  """
  Find (idx, word) tuple out of the field list that is the best candidate for RxBin.
  """
  o = min(enumerate(field_list), key=lambda x: get_distance_to_group(x[1], group))
  # print("o: {}, distance: {}".format(o, get_distance_to_group(o[1], group)))
  return o
