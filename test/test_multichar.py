from lexc_parser.multichar import MulticharSymbols

m = '''Multichar_Symbols +A +N +V  ! +A is adjectives, +N is nouns, +V is verbs
+Adv  ! This one is for adverbs
+Punc ! punctuation
! +Cmpar ! This is broken for now, so I commented it out.

! The bulk of lexc is made of up LEXICONs, which contain entries that point to
! other LEXICONs. "Root" is a reserved lexicon name, and the start state.
! "#" is also a reserved lexicon name, and the end state.

'''


def test_multichar_symbols():
    multichar = MulticharSymbols(m)
    assert repr(multichar) == 'MulticharSymbols(12 symbols, 10 lines)'
