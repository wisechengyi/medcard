import distance

KNOWN_WORDS = {'id', 'rxbin', 'rxgrp', 'issuer', 'first', 'last'}

# for w in KNOWN_WORDS:
#   print(distance.levenshtein(w, 'rx_bin'))

GROUP_RXBIN = {'rxbin', 'rx_bin', 'rx bin'}
GROUP_RXGRP = {'rxgrp', 'rx group', 'rx_grp', 'rxgroup'}


def get_distance_to_group(word, group):
  return min(distance.sorensen(word, x) for x in group)


def get_rx_bin_candidate(field_list):
  return min(field_list, key=lambda x: get_distance_to_group(x, GROUP_RXBIN))
