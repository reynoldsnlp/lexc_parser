from collections import Counter
from collections import OrderedDict
import re
from typing import Dict
from typing import List
import warnings

from .lexicon import Lexicon
from .multichar import MulticharSymbols

__all__ = ['Lexc']


class Lexc:
    """Parent object that represents an entire lexc file."""
    __slots__ = ['_lex_dict', '_upper_expansion_cache', 'end',
                 'multichar_symbols', 'orig', 'prematter']
    _lex_dict: Dict[str, Lexicon]
    _upper_expansion_cache: Dict[str, List[str]]
    end: str
    multichar_symbols: MulticharSymbols
    orig: str
    prematter: str

    def __init__(self, lexc_input: str):
        self._lex_dict = OrderedDict()
        self._lex_dict['#'] = Lexicon('LEXICON #', parent_lexc=self)
        self._upper_expansion_cache = {}
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

        # Change all continuation classes to point to self._lex_dict
        for lex in self._lex_dict.values():
            for entry in lex.entries:
                if isinstance(entry.cc, str):
                    entry.cc = self._lex_dict[entry.cc]

        # Determine which lexicon is root
        if 'Root' not in self._lex_dict:
            self._lex_dict['Root'] = next(iter(self._lex_dict.values()))

        self.end = end

    def __getitem__(self, i):
        return self._lex_dict[i]

    def __iter__(self):
        return (lex for lex in self._lex_dict.values())

    def __repr__(self):
        return f'Lexc(multichars={repr(self.multichar_symbols)}, {len(self._lex_dict)} lexicons)'  # noqa: E501

    def __str__(self):
        return ''.join([self.prematter,
                        str(self.multichar_symbols),
                        '\n\n'.join(str(lex)
                                    for lex in self._lex_dict.values()),
                        self.end])

    def upper_expansions(self, *, cc=None, entry=None, suffix_list=None,
                         tag_delim='+', cc_history=None, max_cycles=0):
        """Expand all uppers in `cc` according to subsequent
        continuation classes. Especially useful for extracting lemmas.
        """
        if cc is None and entry is None:
            cc = self._lex_dict['Root']
        elif not isinstance(cc, Lexicon) and isinstance(cc, str):
            cc = self._lex_dict[cc]
        if cc_history is None:
            cc_history = Counter(['Root'])

        if cc is not None and entry is None and suffix_list is None:
            cc_history.update([cc.id])
            if cc.id in self._upper_expansion_cache:
                expansions = self._upper_expansion_cache[cc.id]
                return expansions
            else:
                suffix_list = ['']
                expansions = []
                for each_entry in cc:
                    if each_entry.cc:
                        if (each_entry.cc.id not in cc_history
                                or cc_history[each_entry.cc.id] < max_cycles):
                            x = self.upper_expansions(entry=each_entry,
                                                      suffix_list=suffix_list,
                                                      tag_delim=tag_delim,
                                                      cc_history=Counter(cc_history),  # noqa: E501
                                                      max_cycles=max_cycles)
                            expansions.extend(x)
                self._upper_expansion_cache[cc.id] = expansions
                return expansions
        elif cc is None and entry is not None and suffix_list is not None:
            if entry.upper is None:
                upper = ''
            else:
                upper = entry.upper.split(tag_delim)[0]
            suffix_list = [f'{lem}{upper}' for lem in suffix_list]
            if not entry.cc:
                pass
            elif entry.cc.id == '#' or (entry.upper is not None
                                        and tag_delim in entry.upper):
                return suffix_list
            else:
                expansions = self.upper_expansions(cc=entry.cc,
                                                   tag_delim=tag_delim,
                                                   cc_history=Counter(cc_history),  # noqa: E501
                                                   max_cycles=max_cycles)
                suffix_list = [f'{lem}{suffix}' for lem in suffix_list
                               for suffix in expansions]
                return suffix_list
        else:
            raise ValueError('upper_expansions accepts cc or entry, not both. '
                             f'cc: {cc}, entry: {entry}, suffix_list: '
                             f'{suffix_list}, tag_delim: {tag_delim}, '
                             f'cc_history: {cc_history}, '
                             f'max_cycles: {max_cycles}')
