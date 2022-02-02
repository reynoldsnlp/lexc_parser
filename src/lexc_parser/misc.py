import re

__all__ = ['escape', 'unescape']


def unescape(in_str) -> str:
    """Unescape all characters preceded by `%`."""
    return re.sub('%(.)', r'\1', in_str or '', flags=re.MULTILINE)


def escape(in_str) -> str:
    """Escape all lexc special characters."""
    return re.sub('([<>#;:!% ])', r'%\1', in_str or '')
