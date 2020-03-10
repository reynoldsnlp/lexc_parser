from collections import namedtuple
import re
from typing import List
import warnings

__all__ = ['MulticharSymbols']

Line = namedtuple('Line', ['symbols', 'comment'])


class MulticharSymbols:
    def __init__(self, multichar_str: str):
        self.symbols: List[str] = []
        self.lines = []
        lines = multichar_str.split('\n')
        for line in lines:
            res = re.search(r'(?:\s*Multichar_Symbols)?((?:%.|[^!])+)?(!.*)?',
                            line)
            if res is not None:
                symbols_str, comment = res.groups(default='')
                symbols = re.split(r'(?!<%)\s+', symbols_str.strip())
                self.symbols.extend(symbols)
                self.lines.append(Line(symbols, comment))
            else:
                warnings.warn(f'bad multichar line: {line!r}',
                              category=SyntaxWarning)

    def __repr__(self):
        return f'MulticharSymbols({len(self.symbols)} symbols, {len(self.lines)} lines)'  # noqa: E501

    def __str__(self):
        lines = '\n'.join([f'{" ".join(line.symbols)} {line.comment}'
                           for line in self.lines])
        return f'Multichar_Symbols\n{lines}'
