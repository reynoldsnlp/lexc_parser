import re


def unescape(in_str):
    """Unescape all characters preceded by `%`."""
    return re.sub('%(.)', r'\1', in_str, re.MULTILINE)


def escape(in_str):
    """Escape all lexc special characters."""
    return re.sub('([<>#;:!])', r'%\1', in_str)
