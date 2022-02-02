from enum import Enum
import re
from typing import Optional

from .misc import unescape

__all__ = ['Comment']


class TestType(Enum):
    NEG = 0
    POS = 1


test_dict = {'$': TestType.NEG,
             '€': TestType.POS}


class Comment:
    __slots__ = ['_comment_str', 'comment', 'reading', 'surface', 'test']
    _comment_str: str
    comment: Optional[str]
    reading: Optional[str]
    surface: Optional[str]
    test: Optional[int]

    def __init__(self, comment_str: str):
        self._comment_str = comment_str
        test_match = re.match(r'!!([€$])\s+((?:%.|[^:])+):\s+(\S+|\S(?:%.|[^#!])*\S)\s*([#!].*)?$', comment_str)
        if test_match:
            test, surface, reading, comment = test_match.groups()
            self.comment = comment
            self.reading = reading
            self.surface = unescape(surface)
            self.test = test_dict[test]
        elif re.match(r'\s*!', comment_str):
            self.comment = comment_str
            self.reading = None
            self.surface = None
            self.test = None
        else:
            raise ValueError(f"Comment string does not begin with '!': {comment_str}")

    def __repr__(self):
        return f'Comment({str(self)})'

    def __str__(self):
        return self._comment_str
