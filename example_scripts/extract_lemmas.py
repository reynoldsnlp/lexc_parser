from collections import defaultdict
from collections import Counter
from itertools import chain
import os
import sys

import ..lexc_parser as lp


try:
    filename = sys.argv[1]
except IndexError:
    HOME = os.environ['HOME']
    filename = HOME + '/gt/lang-rus/src/fst/lexicon.tmp.lexc'


if __name__ == '__main__':
    print('Parsing lexc file...', file=sys.stderr)
    with open(filename) as f:
        lexc = lp.Lexc(f.read())
    print('Extracting lemmas...', file=sys.stderr)
    lemmas = lexc['Propernoun'].upper_expansions()
    c = Counter(lemmas)
    print('lemmas: ', len(lemmas), sorted(lemmas)[:10], 'Борисович' in lemmas)
    print('lemmas: ', len(c), c.most_common(50))
