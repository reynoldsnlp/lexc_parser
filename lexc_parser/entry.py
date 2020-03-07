import re
import warnings
import sys

from .lexicon import _lexicons

__all__ = ['Entry']


class Entry:
    def __init__(self, line):
        line = line.rstrip()
        parsed = re.match(r'''( (?: %. | [^:] )+ )     # capture upper
                              (?: :                    # colon delimiter
                                  ( (?: %. | [^ ] )+ ) # capture lower
                              )?                       # :lower is optional
                              \ +                      # space delimiter(s)
                              ( (?: %. | [^ ;] )+ )    # capture cont class
                              (?: \ "                  # open gloss
                                  ( (?: %. | [^"] )+ ) # capture gloss
                              ")?                      # close gloss
                              \ +;                     # space delimiter(s)
                              ( .* ) $                 # capture comment''',
                          line, re.X)
        if parsed:
            print(parsed, parsed.groups(default=''), file=sys.stderr)  # TODO delete me
            self.is_entry = True
            groups = parsed.groups(default='')
            groups = [re.sub('%(.)', r'\1', elem) for elem in groups]
            self.upper, self.lower, self.cc, self.gloss, self.comment = groups
            if self.cc.isspace():
                warnings.warn(f'bad cont class: {line!r}',
                              category=SyntaxWarning)
            self.cc = _lexicons[self.cc]
            if re.match(r'\s+', self.comment):
                self.comment = ''
            elif self.comment != '' and not re.match(r'\s*!', self.comment):
                warnings.warn(f'bad postmatter: {line!r}',
                              category=SyntaxWarning)
        else:
            self.is_entry = False
            self.upper, self.lower, self.cc, self.gloss = '', '', '', ''
            self.comment = line
            if not re.match(r'\s*!', line):
                warnings.warn(f'bad line: {self.comment}',
                              category=SyntaxWarning)

    def __repr__(self):
        return f'LexiconLine(upper={self.upper}, lower={self.lower}, cc={self.cc}, gloss={self.gloss}, comment={self.comment}'  # noqa: E501

    def __str__(self):
        if self.lower:
            colon = ':'
        else:
            colon = ''
        if self.cc:
            space = ' '
            semi = ' ;'
        else:
            space = ''
            semi = ''
        if self.gloss:
            q1 = ' "'
            q2 = '"'
        else:
            q1 = ''
            q2 = ''
        return f'{self.upper}{colon}{self.lower}{space}{self.cc}{q1}{self.gloss}{q2}{semi}{self.comment}'  # noqa: E501

    def is_comment(self):
        """Return whether comment is the only attribute with a truthy value."""
        return self.comment and not any([self.upper, self.lower, self.cc,
                                         self.gloss])
