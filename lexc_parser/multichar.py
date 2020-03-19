from collections import namedtuple
import re
from typing import List
import warnings

__all__ = ['MulticharSymbols']

Line = namedtuple('Line', ['symbols', 'comment'])


class MulticharSymbols:
    __slots__ = ['lines', 'symbols']
    lines: List[Line]
    symbols: List[str]

    def __init__(self, multichar_str: str):
        self.symbols = []
        self.lines = []
        lines = multichar_str.split('\n')
        for line in lines:
            res = re.search(r'(?:\s*Multichar_Symbols)?\s*((?:%.|[^!])+)?(!.*)?',  # noqa: E501
                            line)
            if res is not None:
                symbols_str, comment = res.groups(default='')
                if symbols_str.strip():
                    symbols = re.split(r'(?!<%)\s+', symbols_str.strip())
                    self.symbols.extend(symbols)
                else:
                    symbols = []
                self.lines.append(Line(symbols, comment))
            else:
                warnings.warn(f'bad multichar line: {line!r}',
                              category=SyntaxWarning)

    def __repr__(self):
        return f'MulticharSymbols({len(self.symbols)} symbols, {len(self.lines)} lines)'  # noqa: E501

    def __str__(self):
        lines = '\n'.join([f'{" ".join(line.symbols)}{line.comment}'
                           for line in self.lines
                           if line.symbols or line.comment])
        if lines:
            return f'Multichar_Symbols\n{lines}\n\n'
        else:
            return ''
