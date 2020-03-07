import re
import warnings

from .lexicon import Lexicon
# from .multichar import MulticharSymbols


class Lexc:
    """Parent object that represents an entire lexc file."""
    __slots__ = ['orig']
    orig: str

    def __init__(self, lexc_input: str):
        self.orig = lexc_input
        parsed = re.match(r'(.*?)(Multichar_Symbols.*?)(LEXICON.*?)(END.*$)',
                          lexc_input, re.MULTILINE)
        prematter, multichar_symbols, lexicons, end = parsed.groups(default='')
        self.prematter = prematter
        if not all(re.match(r'\s*!.*', line)  # if not all lines are comments
                   for line in prematter.split('\n')):
            warnings.warn(f'bad prematter: {prematter}',
                          category=SyntaxWarning)
        # self.multichar_symbols = MulticharSymbols(multichar_symbols)
        self.lexicons = []
        for i, lexicon_str in enumerate(re.split('LEXICON', lexicons)):
            lex = Lexicon(lexicon_str, i=i)
            self.lexicons.append(lex)
        self.end = end
