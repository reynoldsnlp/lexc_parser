from collections import Counter
from collections import OrderedDict
import re
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Set
import warnings

from .lexicon import Lexicon
from .multichar import MulticharSymbols

__all__ = ['Lexc']


class Lexc:
    """Parent object that represents an entire lexc file."""
    __slots__ = ['_lex_dict', 'end', 'multichar_symbols', 'orig', 'prematter']
    _lex_dict: Dict[str, Lexicon]
    end: str
    multichar_symbols: MulticharSymbols
    orig: str
    prematter: str

    def __init__(self, lexc_input: str):
        self._lex_dict = OrderedDict()
        self._lex_dict['#'] = Lexicon('LEXICON #', parent_lexc=self)
        self.orig = lexc_input
        parsed = re.match(r'(.*?)(^[ \t]*Multichar_Symbols.*?)?(^[ \t]*LEXICON.*)$',  # noqa: E501
                          lexc_input, re.DOTALL | re.MULTILINE)
        groups = parsed.groups(default='')  # type: ignore
        prematter, multichar_symbols, lexicons = groups
        if re.search('\n[ \t]*END', lexicons):
            lexicons, end = re.match(r'(.*?)(^[ \t]*END.*)', lexicons,  # type: ignore  # noqa: E501
                                     re.S | re.M).groups(default='')
        else:
            end = ''
        self.prematter = prematter
        if not all(re.match(r'\s*(?:!.*)?', line)  # not all lines are comments
                   for line in prematter.split('\n')):
            warnings.warn(f'bad prematter: {prematter}',
                          category=SyntaxWarning)
        self.multichar_symbols = MulticharSymbols(multichar_symbols)
        for lexicon_str in re.split(r'^LEXICON', lexicons, flags=re.M):
            if lexicon_str:
                lex = Lexicon('LEXICON' + lexicon_str, parent_lexc=self)
                self._lex_dict[lex.id] = lex

        # Determine which lexicon is root
        if 'Root' not in self._lex_dict:
            self._lex_dict['Root'] = next(iter(self._lex_dict.values()))

        self.end = end

    def __getitem__(self, i) -> Optional[Lexicon]:
        return self._lex_dict.get(i)

    def __iter__(self) -> Iterator[Lexicon]:
        return (lex for lex in self._lex_dict.values())

    def __repr__(self):
        return f'Lexc(multichars={repr(self.multichar_symbols)}, {len(self._lex_dict)} lexicons)'  # noqa: E501

    def __str__(self):
        return ''.join([self.prematter,
                        str(self.multichar_symbols),
                        '\n\n'.join(str(lex)
                                    for lex in self._lex_dict.values()),
                        self.end])

    def upper_expansions(self, suffixes=None, tag_delim='+',
                         max_cycles=0) -> Set[str]:
        """Expand all uppers according to subsequent continuation classes.
        Especially useful for extracting lemmas.
        """
        cc = self._lex_dict['Root']
        cc_history = Counter(['Root'])
        return cc.upper_expansions(tag_delim=tag_delim,
                                   cc_history=cc_history,
                                   max_cycles=max_cycles)
