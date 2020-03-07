class Lexc:
    """Parent object that represents an entire lexc file."""
    __slots__ = ['orig']
    orig: str

    def __init__(self, lexc_input: str):
        self.orig = lexc_input
