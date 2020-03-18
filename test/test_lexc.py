import os
import sys

import lexc_parser as lp

expansion_name = os.path.join(os.path.dirname(__file__), 'resources',
                              'upper_expansion.lexc')
with open(expansion_name) as f:
    expansion_str = f.read()


def test_expansion():
    lexc = lp.Lexc(expansion_str)
    print(repr(lexc), lexc.multichar_symbols.symbols, lexc, file=sys.stderr)
    assert set(lexc.upper_expansions()) == {'Boris', 'Borisovic', 'Borisovna',
                                            'Vladimir', 'Vladimirovic',
                                            'Vladimirovna'}
