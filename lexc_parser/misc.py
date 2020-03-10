from collections import defaultdict
import re

__all__ = ['escape', 'unescape']


def unescape(in_str):
    """Unescape all characters preceded by `%`."""
    return re.sub('%(.)', r'\1', in_str, re.MULTILINE)


def escape(in_str):
    """Escape all lexc special characters."""
    return re.sub('([<>#;:!])', r'%\1', in_str)


class keydefaultdict(defaultdict):
    """defaultdict that uses key to produce the default value."""
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
