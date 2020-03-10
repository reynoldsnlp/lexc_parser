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
    assert repr(lexc1.multichar_symbols) == 'MulticharSymbols(12 symbols, 10 lines)'  # noqa: E501
    assert len(lexc1.lexicons) == 8
    assert repr(lexc1.lexicons) == '[Lexicon(id=Root, entries=22), Lexicon(id=Adj, entries=4), Lexicon(id=Adv, entries=3), Lexicon(id=Noun, entries=4), Lexicon(id=Num_start, entries=3), Lexicon(id=Num, entries=4), Lexicon(id=Verb, entries=4), Lexicon(id=Punctuation, entries=3)]'  # noqa: E501
    assert lexc1.end == 'END\n\nThis text is ignored because it is after END\n'
