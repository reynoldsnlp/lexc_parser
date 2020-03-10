import re
import sys
import warnings

from .lexicon import Lexicon
from .misc import keydefaultdict
from .multichar import MulticharSymbols

__all__ = ['Lexc']


class Lexc:
    """Parent object that represents an entire lexc file."""
    __slots__ = ['_lexicon_dict', 'end', 'lexicons', 'multichar_symbols',
                 'orig', 'prematter']
    orig: str

    def __init__(self, lexc_input: str):
        self._lexicon_dict = keydefaultdict(lambda x: x)  # type: ignore
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
        for group in [prematter, multichar_symbols, lexicons, end]:
            print(repr(group), file=sys.stderr)
            print('='*79, file=sys.stderr)
        self.prematter = prematter
        if not all(re.match(r'\s*(?:!.*)?', line)  # not all lines are comments
                   for line in prematter.split('\n')):
            warnings.warn(f'bad prematter: {prematter}',
                          category=SyntaxWarning)
        self.multichar_symbols = MulticharSymbols(multichar_symbols)
        self.lexicons = []
        for lexicon_str in re.split(r'^LEXICON', lexicons, flags=re.M):
            if lexicon_str:
                lex = Lexicon('LEXICON' + lexicon_str)
                self.lexicons.append(lex)

        # Change all continuation classes to point to self._lexicon_dict
        for lex in self.lexicons:
            self._lexicon_dict[lex.id] = lex
        for lex in self.lexicons:
            for entry in lex.entries:
                entry.cc = self._lexicon_dict[entry.cc]

        # Determine which lexicon is root
        if 'Root' not in self._lexicon_dict:
            self._lexicon_dict['Root'] = self.lexicons[0]

        self.end = end

    def __repr__(self):
        return f'Lexc(multichars={self.multichar_symbols!r}, {len(self.lexicons)} lexicons)'  # noqa: E501

    def __str__(self):
        return '\n\n'.join([self.prematter,
                            str(self.multichar_symbols),
                            '\n\n'.join(str(lex) for lex in self.lexicons),
                            self.end])
