import re
import warnings
from .misc import escape
from .misc import unescape

__all__ = ['Entry']


class Entry:
    def __init__(self, line):
        parsed = re.match(r'''\s*(?:                      # open upper
                                  ( (?: %. | [^ \t:] )+ | # capture upper...
                                   < (?: %. | [^>] )+ > ) # ... or regex
                              )?                          # upper is optional
                              (?: :                     # colon delim for lower
                                  ( (?: %. | [^ \t] )+ )  # capture lower
                              )?                          # :lower is optional
                              [ \t]+                      # space delimiter(s)
                              ( (?: %. | [^ ;] )+ )       # capture cont class
                              (?: [ \t]+"                 # open gloss
                                  ( (?: %. | [^"] )+ )    # capture gloss
                              ")?                         # close gloss
                              [ \t]+;                     # space delimiter(s)
                              ( .*? ) \s* $               # capture comment''',
                          line, re.X)
        if parsed:
            self.is_entry = True
            groups = parsed.groups(default='')
            self.upper, self.lower, self.cc, self.gloss, self.comment = groups
            if re.match(r'<(?:%.|[^>])+>', self.upper):
                self.regex = True
            else:
                self.regex = False
                self.upper = unescape(self.upper)
            self.lower = unescape(self.lower)
            assert (self.upper and self.lower and self.cc  # upper:lower entry
                    or self.upper and not self.lower and self.cc  # simple string entry or xfst regex  # noqa: E501
                    or not self.upper and not self.lower and self.cc), f'bad entry: {line!r}'  # empty data entry  # noqa: E501
            if self.cc.isspace():
                warnings.warn(f'bad cont class: {line!r}',
                              category=SyntaxWarning)
            if re.match(r'\s+', self.comment):
                self.comment = ''
            elif self.comment != '' and not re.match(r'\s*!', self.comment):
                warnings.warn(f'bad postmatter: {line!r}',
                              category=SyntaxWarning)
        else:
            self.is_entry = False
            self.regex = False
            self.upper, self.lower, self.cc, self.gloss = '', '', '', ''
            self.comment = line
            if not re.match(r'\s*(?:!)?', line):
                warnings.warn(f'bad line: {self.comment}',
                              category=SyntaxWarning)

    def __repr__(self):
        return f'LexiconLine(upper={self.upper}, lower={self.lower}, cc={self.cc}, gloss={self.gloss}, comment={self.comment}'  # noqa: E501

    def __str__(self):
        return (f'{escape(self.upper) if not self.regex else self.upper}'
                f'{":" if self.lower else ""}'
                f'{escape(self.lower)}'
                f'{" " if self.cc else ""}'
                f'{self.cc}'  # TODO escape() this?
                f'''{' "' if self.gloss else ''}'''
                f'{self.gloss}'  # TODO escape() this?
                f'''{'"' if self.gloss else ''}'''
                f'{" ;" if self.cc else ""}'
                f'{self.comment}')

    def is_comment(self):
        """Return whether comment is the only attribute with a truthy value."""
        return self.comment and not any([self.upper, self.lower, self.cc,
                                         self.gloss])
