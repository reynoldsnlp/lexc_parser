from collections import Counter
import re
from typing import List
from typing import Optional
from typing import Set
from typing import TYPE_CHECKING
import warnings

from .misc import escape
from .misc import unescape

if TYPE_CHECKING:
    from .lexicon import Lexicon

__all__ = ['Entry']


class Entry:
    __slots__ = ['_cc', 'comment', 'gloss', 'is_comment', 'is_entry',
                 'is_regex', 'lower', 'parent_lexc', 'parent_lexicon', 'upper']
    _cc: str
    comment: str
    gloss: str
    is_comment: bool
    is_entry: bool
    is_regex: bool
    lower: str
    parent_lexicon: 'Lexicon'
    upper: str

    def __init__(self, line, parent_lexicon=None):
        parsed = self._parse_entry(line)
        if parsed:
            self.is_entry = True
            self.is_comment = False
            self.upper, self.lower, self._cc, self.gloss, self.comment = parsed
            if re.match(r'<(?:%.|[^>])+>', self.upper or ''):
                self.is_regex = True
            else:
                self.is_regex = False
                self.upper = unescape(self.upper or '') or None
            self.lower = unescape(self.lower or '') or None
            assert self.lower is None or self.lower.startswith(':')
            assert (  # non-entry
                    not any([self.upper, self.lower, self._cc])
                      # upper:lower cc ;
                    or self.upper and self.lower and self._cc
                      # upper cc ;  OR  < r e g e x > cc ;
                    or self.upper and not self.lower and self._cc
                      # cc ;
                    or not self.upper and not self.lower and self._cc), f'bad entry: {line!r}'  # noqa: E501
            if self._cc and self._cc.isspace():
                warnings.warn(f'bad cont class: {line!r}',
                              category=SyntaxWarning)
            if re.match(r'\s*$', self.comment or ''):
                self.comment = None
            elif not re.match(r'\s*!', self.comment):
                warnings.warn(f'bad postmatter: {line!r} {self.comment!r}',
                              category=SyntaxWarning)
        else:
            self.is_entry = False
            self.is_regex = False
            self.upper, self.lower, self._cc, self.gloss = [None] * 4
            self.comment = line
            if re.match(r'\s*(?:!)?', line):
                self.is_comment = True
            else:
                self.is_comment = False
                warnings.warn(f'bad line: {self.comment}',
                              category=SyntaxWarning)
        self.parent_lexicon = parent_lexicon
        if parent_lexicon is not None:
            self.parent_lexc = parent_lexicon.parent_lexc
        else:
            self.parent_lexc = None

    @property
    def cc(self) -> 'Lexicon':
        return self.parent_lexc[self._cc]

    def __repr__(self):
        try:
            return f'Entry(upper={self.upper}, lower={self.lower}, cc={self.cc.id}, gloss={self.gloss}, comment={self.comment})'  # noqa: E501
        except AttributeError:
            return repr(self.__dict__)

    def __str__(self):
        if self._cc is not None:
            return (f'{escape(self.upper or "") if not self.is_regex else self.upper}'  # noqa: E501
                    # f'{":" if self.lower else ""}'
                    f'{escape(self.lower)[1:]}'
                    f'{" " if self.upper or self.lower else ""}'
                    f'{self._cc}'  # TODO escape() this?
                    f'''{' "' if self.gloss else ''}'''
                    f'{self.gloss or ""}'  # TODO escape() this?
                    f'''{'"' if self.gloss else ''}'''
                    f'{" ;" if self._cc else ""}'
                    f'{self.comment or ""}')
        else:
            return self.comment or ''

    @staticmethod
    def _parse_entry(line) -> Optional[List[Optional[str]]]:
        upper_lower_re = r'''(?:                         # open full-spec data
                             ( (?: %. | [^:!] )+ )       # capture upper
                             ( : (?: %. | [^ \t!] )* )   # capture lower
                             [ \t]+                      # space delimiter(s)
                             )                           # close full-spec data
                             '''
        upper_re = r'''(?:                         # open simple data
                       ( (?: %. | [^ \t:!] )+ |    # capture upper...
                         < (?: %. | [^>] )+ > )    # ... or regex
                       ()                          # capture lower
                       [ \t]+                      # space delimiter(s)
                       )                           # close simple data
                       '''
        data_re = fr'''(?:                          # open data
                          [ \t]*                    # leading whitespace?
                          {upper_lower_re}          # upper:lower
                          |                         # OR
                          {upper_re}                # upper
                          |                         # OR
                          (?: ()() [ \t]*)          # capture no-data
                        )                           # close data
                        '''
        cc_re = r'''(?:                           # open cc
                         ( (?: %. | [^ \t!] )+ )  # capture cont class
                         [ \t]+                   # space delimiter(s)
                      )                           # close cc
                    '''
        gloss_re = r'''(?:                        # open optnl gloss statment
                      (?: "                       # open gloss
                      ( (?: %. | [^"] )+ )        # capture gloss
                      " [ \t]+ )                  # close gloss
                         |                        # OR
                      ()                          # empty gloss
                      )?                          # close optnl gloss sttment
                      '''
        all_re = fr'''(?:                            # open entry
                         {data_re}                   # (upper(:lower))
                      (?:                            # open final
                         (?: {cc_re} {gloss_re} ; )  # open cc statement
                         |                           # OR
                         ()()                        # empty cc and gloss
                      )                              # close final
                      )                              # close entry
                      (?: ( \s*!.*? ) | () ) \s* $   # capture comment
                      '''

        parsed = re.match(all_re, line, re.X)
        if parsed:
            groups = [g or None for g in parsed.groups() if g is not None]
            return groups
        else:
            return None

    def upper_expansions(self, suffixes=None, tag_delim='+', cc_history=None,
                         max_cycles=0) -> Set[str]:
        """Expand self.upper according to subsequent continuation classes.
        Especially useful for extracting lemmas.
        """
        if self.upper is None:
            upper = ''
        else:
            upper = self.upper.split(tag_delim)[0]
        suffixes = {f'{lem}{upper}' for lem in suffixes}
        if self.cc.id == '#' or (self.upper is not None
                                 and tag_delim in self.upper):
            return suffixes
        else:
            expansions = self.cc.upper_expansions(tag_delim=tag_delim,
                                                  # new instance of cc_history
                                                  cc_history=Counter(cc_history),  # noqa: E501
                                                  max_cycles=max_cycles)
            return {f'{lem}{suffix}' for lem in suffixes
                    for suffix in expansions}
