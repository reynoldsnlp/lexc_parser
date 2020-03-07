import lexc_parser as lp


entry_strs = [('a:b c ;\n', ('a', 'b', 'c', '')),
              ('a%::b c "d" ;\n', ('a:', 'b', 'c', 'd')),
              ('a%%:b c ;\n', ('a%', 'b', 'c', '')),
              ('a%%%::b c "d" ;\n', ('a%:', 'b', 'c', 'd'))]


def test_escaping():
    for line, parse in entry_strs:
        e = lp.Entry(line)
        assert (e.upper, e.lower, e.cc, e.gloss) == parse
