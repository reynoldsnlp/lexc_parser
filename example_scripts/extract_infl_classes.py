"""Extract lemmas and inflection classes."""

import os
import re
import sys

import lexc_parser as lp


try:
    filename = sys.argv[1]
except IndexError:
    HOME = os.environ['HOME']
    filename = HOME + '/gt/lang-rus/src/fst/lexicon.tmp.lexc'

print('Parsing lexc file...', file=sys.stderr)
with open(filename) as f:
    src = f.read()
lexc = lp.Lexc(src)

primary_lexicons = [entry.cc.id for entry in lexc['Root']
                    if entry.cc is not None and entry.cc.id != 'Numeral']
V_cc_lemmas_dict = lexc['Verb'].cc_lemmas_dict
N_cc_lemmas_dict = lexc['Noun'].cc_lemmas_dict
print(len(V_cc_lemmas_dict))
print([(cc, len(lemmas)) for cc, lemmas in V_cc_lemmas_dict.items()])
with open('Verbs_conjugation_classes.tsv', 'w') as f:
    for cc, lemmas in V_cc_lemmas_dict.items():
        try:
            simple_cc = re.search(r'_([0-9]+)°?[a-c]', cc).group(1)
        except AttributeError:
            simple_cc = '???'
        for lemma in lemmas:
            print(simple_cc, cc, lemma, sep='\t', file=f)
