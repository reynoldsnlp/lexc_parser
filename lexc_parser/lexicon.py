import re

from .entry import Entry

__all__ = ['Lexicon']
NEWLINE = '\n'


class Lexicon:
    def __init__(self, lex: str, parent_lexc=None):
        self.parent_lexc = parent_lexc
        lines = lex.split('\n')
        first_line = re.search(r'LEXICON[ \t]+((?:%.|[^ \t!])+)[ \t]*(.*)$',
                               lines[0])
        self.id, self.comment = first_line.groups(default='')  # type: ignore
        self.entries = [Entry(line, parent_lexicon=self) for line in lines[1:]]

    def __getitem__(self, i):
        return self.entries[i]

    def __iter__(self):
        return (e for e in self.entries)

    def __repr__(self):
        return f'Lexicon(id={self.id}, entries={len(self.entries)})'

    def __str__(self):
        str_entries = [str(e) for e in self.entries]
        return f'LEXICON {self.id}{NEWLINE}{NEWLINE.join(str_entries)}'
