# lexc\_parser

An object-oriented approach to filtering, modifying, or extracting information from lexc with an opinionated reformatter.


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

LEXICON Verbs
work:work reg_verb ;
talk:talk reg_verb ;

LEXICON reg_noun ;
+Sg: # ;
+Pl:s # ;

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
print(sorted(lexc.upper_expansions(cc='Nouns')))  # extract lemmas from Nouns
# ['cat', 'dog']
```
