import os

import lexc_parser as lp

ex1_name = os.path.join(os.path.dirname(__file__), 'resources', 'ex1.lexc')
with open(ex1_name) as f:
    ex1 = f.read()
ex2_name = os.path.join(os.path.dirname(__file__), 'resources', 'ex2.lexc')
with open(ex2_name) as f:
    ex2 = f.read()


def test_ex1():
    lexc1 = lp.lexc.Lexc(ex1)
    assert repr(lexc1.multichar_symbols) == 'MulticharSymbols(5 symbols, 10 lines)'  # noqa: E501
    assert len(lexc1._lex_dict) == 9
    assert repr(lexc1._lex_dict) == "OrderedDict([('#', Lexicon(id=#, entries=0)), ('Root', Lexicon(id=Root, entries=22)), ('Adj', Lexicon(id=Adj, entries=4)), ('Adv', Lexicon(id=Adv, entries=3)), ('Noun', Lexicon(id=Noun, entries=4)), ('Num_start', Lexicon(id=Num_start, entries=3)), ('Num', Lexicon(id=Num, entries=4)), ('Verb', Lexicon(id=Verb, entries=4)), ('Punctuation', Lexicon(id=Punctuation, entries=3))])"  # noqa: E501
    assert lexc1.end == 'END\n\nThis text is ignored because it is after END\n'
