import re
import sys
import warnings

from .misc import escape
from .misc import unescape

__all__ = ['Entry']


class Entry:
    def __init__(self, line, parent_lexicon=None):
        parsed = self._parse_entry(line)
        if parsed:
            self.is_entry = True
            self.is_comment = False
            self.upper, self.lower, self.cc, self.gloss, self.comment = parsed
            if re.match(r'<(?:%.|[^>])+>', self.upper or ''):
                self.regex = True
            else:
                self.regex = False
                self.upper = unescape(self.upper or '') or None
            self.lower = unescape(self.lower or '') or None
            assert self.lower is None or self.lower.startswith(':')
            assert (  # non-entry
                    not any([self.upper, self.lower, self.cc])
                      # upper:lower cc ;
                    or self.upper and self.lower and self.cc
                      # upper cc ;  OR  < r e g e x > cc ;
                    or self.upper and not self.lower and self.cc
                      # cc ;
                    or not self.upper and not self.lower and self.cc), f'bad entry: {line!r}'  # noqa: E501
            if self.cc and self.cc.isspace():
                warnings.warn(f'bad cont class: {line!r}',
                              category=SyntaxWarning)
            if re.match(r'\s*$', self.comment or ''):
                self.comment = None
            elif not re.match(r'\s*!', self.comment):
                warnings.warn(f'bad postmatter: {line!r} {self.comment!r}',
                              category=SyntaxWarning)
        else:
            self.is_entry = False
            self.regex = False
            self.upper, self.lower, self.cc, self.gloss = [None] * 4
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

    def __repr__(self):
        try:
            return f'Entry(upper={self.upper}, lower={self.lower}, cc={self.cc.id}, gloss={self.gloss}, comment={self.comment})'  # noqa: E501
        except AttributeError:
            return repr(self.__dict__)

    def __str__(self):
        if self.cc:
            return (f'{escape(self.upper or "") if not self.regex else self.upper}'  # noqa: E501
                    f'{":" if self.lower else ""}'
                    f'{escape(self.lower)[1:]}'
                    f'{" " if self.cc else ""}'
                    f'{self.cc.id}'  # TODO escape() this?
                    f'''{' "' if self.gloss else ''}'''
                    f'{self.gloss or ""}'  # TODO escape() this?
                    f'''{'"' if self.gloss else ''}'''
                    f'{" ;" if self.cc else ""}'
                    f'{self.comment or ""}')
        else:
            return self.comment or ''

    @staticmethod
    def _parse_entry(line):
        upper_lower_re = r'''(?:                         # open full-spec data
                             ( (?: %. | [^:] )+ )        # capture upper
                             ( : (?: %. | [^ \t] )* )    # capture lower
                             [ \t]+                      # space delimiter(s)
                             )                           # close full-spec data
                             '''
        upper_re = r'''(?:                         # open simple data
                       ( (?: %. | [^ \t:] )+ |     # capture upper...
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
                         ( (?: %. | [^ \t] )+ )   # capture cont class
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
            print('_parse_entry:', repr(line), parsed.groups(), groups,
                  file=sys.stderr)
            return groups
        else:
            print('_parse_entry:', repr(line), repr(None), file=sys.stderr)
            return None

    def expand_upper(self, tag_delim='+'):
        """Follow all continuation classes to build complete lemma."""
        return [f'{self.upper}{suffix}'
                for suffix in self.parent_lexc.upper_expansions(self.cc)]
