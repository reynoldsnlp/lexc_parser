import lexc_parser as lp


entry_strs = [('a:b\t   c         ;\n', ('a', 'b', 'c', '')),
              ('a%::b   c "d"     ;\n', ('a:', 'b', 'c', 'd')),
              ('a%%:b   c         ;\n', ('a%', 'b', 'c', '')),
              ('a%%%::b c "d"     ;\n', ('a%:', 'b', 'c', 'd')),
              ('a       c         ;\n', ('a', '', 'c', '')),
              ('a       c         ;  ', ('a', '', 'c', '')),
              ('        c         ;  ', ('', '', 'c', '')),
              ('< a b* c+ (d) > c ;\n', ('< a b* c+ (d) >', '', 'c', '')),
              ('< a b* %> c (d) > c ;\n', ('< a b* %> c (d) >', '', 'c', '')),
              ]


def test_escaping():
    for line, parse in entry_strs:
        e = lp.Entry(line)
        assert (e.upper, e.lower, e.cc, e.gloss) == parse
