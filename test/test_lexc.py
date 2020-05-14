import os

import lexc_parser as lp

expansion_name = os.path.join(os.path.dirname(__file__), 'resources',
                              'upper_expansion.lexc')
with open(expansion_name) as f:
    expansion_str = f.read()


def test_expansion():
    lexc = lp.Lexc(expansion_str)
    assert lexc['Male'].upper_expansions() == {'', 'ovic', 'ovna'}
    assert lexc['Pat'].entries[0].upper_expansions() == {'ic'}
    assert lexc.upper_expansions() == {'Boris', 'Borisovic', 'Borisovna',
                                       'Bo ris', 'Bo risovic',
                                       'Bo risovna', 'Vladimir',
                                       'Vladimirovic', 'Vladimirovna'}
