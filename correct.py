import distance

KNOWN_WORDS = {'id', 'rxbin', 'rxgrp', 'issuer', 'first', 'last'}

for w in KNOWN_WORDS:
  print(distance.levenshtein(w, 'rx_bin'))

