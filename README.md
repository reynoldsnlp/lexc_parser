# lexc\_parser

An object-oriented approach to filtering, modifying, or extracting information
from lexc with an opinionated reformatter.


## Installation

This package can be installed using...

```bash
$ python -m pip install --user git+https://github.com/reynoldsnlp/lexc_parser
```

## Usage

```python
from lexc_parser import Lexc

src = '''LEXICON Root
Nouns ;
Verbs ;

LEXICON Nouns
cat:cat reg_noun ;
dog:dog reg_noun ;

LEXICON reg_noun ;
+Sg: # ;
+Pl:s # ;

LEXICON Verbs
work:work reg_verb ;
tal:tal k_reg_verb ;

LEXICON k_reg_verb
k:k reg_verb ;

LEXICON reg_verb ;
+Prs+1p+Sg: # ;
+Prs+1p+Pl: # ;
+Prs+2p+Sg: # ;
+Prs+2p+Pl: # ;
+Prs+3p+Sg:s # ;
+Prs+3p+Pl: # ;
+Pst:ed # ;
'''

lexc = Lexc(src)
print(sorted(lexc.upper_expansions()))  # extract lemmas
# ['cat', 'dog', 'talk', 'work']
print(sorted(lexc['Nouns'].upper_expansions()))  # extract lemmas from Nouns
# ['cat', 'dog']
print(lexc['Verbs'].cc_lemmas_dict == {'reg_verb': {'work'}, 'k_reg_verb': {'talk'}})  # dictionary of classes
# True
print(lexc['Root'].cc_lemmas_dict == {'Nouns': {'cat', 'dog'}, 'Verbs': {'work', 'talk'}})  # dictionary of classes
# True
```
