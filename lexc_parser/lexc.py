import re
import sys
from typing import Dict
from typing import List
import warnings

from .lexicon import Lexicon
from .misc import keydefaultdict
from .multichar import MulticharSymbols

__all__ = ['Lexc']


class Lexc:
    """Parent object that represents an entire lexc file."""
    __slots__ = ['_lexicon_dict', '_upper_expansion_cache', 'end', 'lexicons',
                 'multichar_symbols', 'orig', 'prematter']
    orig: str
    _upper_expansion_cache: Dict[str, List[str]]

    def __init__(self, lexc_input: str):
        self._lexicon_dict = keydefaultdict(lambda x: x)  # type: ignore
        self._lexicon_dict['#'] = Lexicon('LEXICON #', parent_lexc=self)
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
        self.lexicons = []
        for lexicon_str in re.split(r'^LEXICON', lexicons, flags=re.M):
            if lexicon_str:
                lex = Lexicon('LEXICON' + lexicon_str, parent_lexc=self)
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

    def __getitem__(self, i):
        return self._lexicon_dict[i]

    def __iter__(self):
        return (lex for lex in self.lexicons)

    def __repr__(self):
        return f'Lexc(multichars={self.multichar_symbols!r}, {len(self.lexicons)} lexicons)'  # noqa: E501

    def __str__(self):
        return ''.join([self.prematter,
                        str(self.multichar_symbols),
                        '\n\n'.join(str(lex) for lex in self.lexicons),
                        self.end])

    def upper_expansions(self, *, cc=None, entry=None, suffix_list=None,
                         tag_delim='+'):
        """Expand all uppers in `cc` according to subsequent
        continuation classes. Especially useful for extracting lemmas.
        """
        if not cc and not entry:
            cc = self._lexicon_dict['Root']

        if cc is not None and entry is None and suffix_list is None:
            try:
                return self._upper_expansion_cache[cc.id]
            except KeyError:
                suffix_list = ['']
                new_suffix_list = []
                for each_entry in cc:
                    if each_entry.cc:
                        expansions = self.upper_expansions(entry=each_entry,
                                                           suffix_list=suffix_list,
                                                           tag_delim=tag_delim)
                        new_suffix_list.extend(expansions)
                self._upper_expansion_cache[cc.id] = new_suffix_list
                return new_suffix_list
        elif cc is None and entry is not None and suffix_list is not None:
            result = re.match(fr'((?:%.|[^ +])+)({re.escape(tag_delim)}?)',
                              entry.upper or '')
            if result is not None:
                upper, delim = result.groups()
            else:
                upper, delim = '', ''
            # TODO this regex not robust against a regex entries. Problem?
            suffix_list = [f'{lem}{upper}' for lem in suffix_list]
            if not entry.cc:
                pass
            elif entry.cc.id == '#' or delim != '':
                return suffix_list
            else:
                expansions = self.upper_expansions(cc=entry.cc,
                                                   tag_delim=tag_delim)
                suffix_list = [f'{lem}{suffix}' for lem in suffix_list
                               for suffix in expansions]
                return suffix_list
        else:
            raise ValueError('upper_expansions accepts cc or entry, not both.')
