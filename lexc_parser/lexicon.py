import re

from .entry import Entry

__all__ = ['Lexicon']
NEWLINE = '\n'


class Lexicon:
    def __init__(self, lex: str):
        lines = lex.split('\n')
        first_line = re.search(r'LEXICON\s+((?:%.|[^ \t!])+)\s*(.*)$',
                               lines[0])
        self.id, self.comment = first_line.groups(default='')  # type: ignore
        self.entries = [Entry(line) for line in lines[1:]]

    def __repr__(self):
        return f'Lexicon(id={self.id}, entries={len(self.entries)})'

    def __str__(self):
        str_entries = [f'{e!s}' for e in self.entries]
        return f'LEXICON {self.id}{NEWLINE}{NEWLINE.join(str_entries)}'
