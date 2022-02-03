from collections import defaultdict
import re
from typing import Counter
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import TYPE_CHECKING
from warnings import warn

from .entry import Entry
if TYPE_CHECKING:
    from .lexc import Lexc

__all__ = ['Lexicon']
NEWLINE = '\n'


class Lexicon:
    __slots__ = ['_cc_lemmas_dict', '_upper_expansions', 'comment', 'entries',
                 'id', 'parent_lexc']
    _cc_lemmas_dict: Optional[Dict[str, Set[str]]]
    _upper_expansions: Optional[Set[str]]
    comment: str
    entries: List[Entry]
    id: str
    parent_lexc: 'Lexc'

    def __init__(self, lex: str, parent_lexc=None):
        self._cc_lemmas_dict = None
        self._upper_expansions = None
        self.parent_lexc = parent_lexc
        lines = lex.split('\n')
        first_line = re.search(r'LEXICON[ \t]+((?:%.|[^ \t!])+)[ \t]*(.*)$',
                               lines[0])
        self.id, self.comment = first_line.groups(default='')  # type: ignore
        self.entries = [Entry(line, parent_lexicon=self) for line in lines[1:]]

    def __getitem__(self, i) -> Entry:
        return self.entries[i]

    def __iter__(self) -> Iterator[Entry]:
        return (e for e in self.entries)

    def __repr__(self):
        return f'Lexicon(id={self.id}, entries={len(self.entries)})'

    def __str__(self):
        str_entries = [str(e) for e in self.entries]
        return f'LEXICON {self.id}{NEWLINE}{NEWLINE.join(str_entries)}'

    def upper_expansions(self,
                         tag_delim='+',
                         cc_history: Optional[Counter[str]] = None,
                         max_cycles=0) -> Set[str]:
        """Expand all uppers in `cc` according to subsequent
        continuation classes. Especially useful for extracting lemmas.
        """
        if cc_history is None:
            cc_history = Counter()
        cc_history.update([self.id])
        if self._upper_expansions is not None:
            return self._upper_expansions
        else:
            suffixes: Set[str] = set()
            self._upper_expansions = set()
            for each_entry in self:
                if each_entry.cc is not None:
                    if (each_entry.cc.id not in cc_history
                            or cc_history[each_entry.cc.id] < max_cycles):
                        x = each_entry.upper_expansions(suffixes=suffixes,
                                                        tag_delim=tag_delim,
                                                        # new instance of cc_history  # noqa: E501
                                                        cc_history=Counter(cc_history),  # noqa: E501
                                                        max_cycles=max_cycles)
                        self._upper_expansions.update(x)
            return self._upper_expansions

    def cc_lemmas_dict(self, tag_delim='+',
                       max_cycles=0) -> Dict[str, Set[str]]:
        """Dictionary showing all the lemmas that use the same continuation
        class.
        """
        if self._cc_lemmas_dict is not None:
            return self._cc_lemmas_dict
        self._cc_lemmas_dict = defaultdict(set)
        dups = set()
        for entry in self:
            if entry.cc is not None:
                upp_exp = entry.upper_expansions(tag_delim=tag_delim,
                                                 max_cycles=max_cycles)
                for ue in upp_exp:
                    if ue in self._cc_lemmas_dict[entry.cc.id]:
                        dups.add(ue)
                self._cc_lemmas_dict[entry.cc.id].update(upp_exp)
        if dups:
            warn(f'Lemmas declared more than once within {self.id}:\n{dups}',
                 stacklevel=2)
        self._cc_lemmas_dict = dict(self._cc_lemmas_dict)
        return self._cc_lemmas_dict
