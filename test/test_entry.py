import lexc_parser as lp


entries = [('a:b\t   c         ;\n', ['a', ':b', 'c', None, None]),
           ('a:b\t c ;\n', ['a', ':b', 'c', None, None]),
           ('a:b\t c ;', ['a', ':b', 'c', None, None]),
           ('a%::b   c "d"     ;\n', ['a%:', ':b', 'c', 'd', None]),
           ('a%::b c "d" ;\n', ['a%:', ':b', 'c', 'd', None]),
           ('a%::b c "d" ;', ['a%:', ':b', 'c', 'd', None]),
           ('a%%:b   c         ;\n', ['a%%', ':b', 'c', None, None]),
           ('a%%:b c ;\n', ['a%%', ':b', 'c', None, None]),
           ('a%%:b c ;', ['a%%', ':b', 'c', None, None]),
           ('a%%%::b c "d"     ;\n', ['a%%%:', ':b', 'c', 'd', None]),
           ('a%%%::b c "d" ;\n', ['a%%%:', ':b', 'c', 'd', None]),
           ('a%%%::b c "d" ;', ['a%%%:', ':b', 'c', 'd', None]),
           ('a       c         ;\n', ['a', None, 'c', None, None]),
           ('a c ;\n', ['a', None, 'c', None, None]),
           ('a c ;', ['a', None, 'c', None, None]),
           ('a       c         ;  ', ['a', None, 'c', None, None]),
           ('a c ;  ', ['a', None, 'c', None, None]),
           ('a c ;', ['a', None, 'c', None, None]),
           ('        c         ;  ', [None, None, 'c', None, None]),
           ('c ;  ', [None, None, 'c', None, None]),
           ('c ;', [None, None, 'c', None, None]),
           ('< a b* c+ (d) > c ;\n', ['< a b* c+ (d) >', None, 'c', None, None]),
           ('< a b* %> c (d) > c ;\n', ['< a b* %> c (d) >', None, 'c', None, None]),
           ('ic+Msc:ic ProperNoun ;', ['ic+Msc', ':ic', 'ProperNoun', None, None]),
           ('na+Fem:na ProperNoun ;', ['na+Fem', ':na', 'ProperNoun', None, None]),
           ('+N+Prop: # ;', ['+N+Prop', ':', '#', None, None]),
           (':b c ;', [None, ':b', 'c', None, None]),
           (':b c ;\t ! comment', [None, ':b', 'c', None, '\t ! comment']),
           (' :b c ;\t ! comment', [None, ':b', 'c', None, '\t ! comment']),
           (' a c ;', ['a', None, 'c', None, None]),
           ]


def test_parse_entry():
    for entry, analysis in entries:
        assert entry and lp.Entry._parse_entry(entry) == analysis


def test_str():
    assert str(lp.Entry('a:b\t   c         ;\n')) == 'a:b c ;'
    assert str(lp.Entry('a:b\t c ;\n')) == 'a:b c ;'
    assert str(lp.Entry('a:b\t c ;')) == 'a:b c ;'
    assert str(lp.Entry('a%::b   c "d"     ;\n')) == 'a%::b c "d" ;'
    assert str(lp.Entry('a%::b c "d" ;\n')) == 'a%::b c "d" ;'
    assert str(lp.Entry('a%::b c "d" ;')) == 'a%::b c "d" ;'
    assert str(lp.Entry('a%%:b   c         ;\n')) == 'a%%:b c ;'
    assert str(lp.Entry('a%%:b c ;\n')) == 'a%%:b c ;'
    assert str(lp.Entry('a%%:b c ;')) == 'a%%:b c ;'
    assert str(lp.Entry('a%%%::b c "d"     ;\n')) == 'a%%%::b c "d" ;'
    assert str(lp.Entry('a%%%::b c "d" ;\n')) == 'a%%%::b c "d" ;'
    assert str(lp.Entry('a%%%::b c "d" ;')) == 'a%%%::b c "d" ;'
    assert str(lp.Entry('a       c         ;\n')) == 'a c ;'
    assert str(lp.Entry('a c ;\n')) == 'a c ;'
    assert str(lp.Entry('a c ;')) == 'a c ;'
    assert str(lp.Entry('a       c         ;  ')) == 'a c ;'
    assert str(lp.Entry('a c ;  ')) == 'a c ;'
    assert str(lp.Entry('a c ;')) == 'a c ;'
    assert str(lp.Entry('        c         ;  ')) == 'c ;'
    assert str(lp.Entry('c ;  ')) == 'c ;'
    assert str(lp.Entry('c ;')) == 'c ;'
    assert str(lp.Entry('< a b* c+ (d)) > c ;\n')) == '< a b* c+ (d)) > c ;'
    assert str(lp.Entry('< a b* %> c (d)) > c ;')) == '< a b* %> c (d)) > c ;'
    assert str(lp.Entry('Boris Male ;')) == 'Boris Male ;'
    assert str(lp.Entry('Vladimir Male ;')) == 'Vladimir Male ;'
    assert str(lp.Entry('ProperNoun ;')) == 'ProperNoun ;'
    assert str(lp.Entry('ov Pat ;')) == 'ov Pat ;'
    assert str(lp.Entry('ic+Msc:ic ProperNoun ;')) == 'ic+Msc:ic ProperNoun ;'
    assert str(lp.Entry('na+Fem:na ProperNoun ;')) == 'na+Fem:na ProperNoun ;'
    assert str(lp.Entry('+N+Prop: # ;')) == '+N+Prop: # ;'
    assert str(lp.Entry(':b c ;')) == ':b c ;'
    assert str(lp.Entry(':b c ;\t ! comment')) == ':b c ;\t ! comment'
    assert str(lp.Entry(' :b c ;\t ! comment')) == ':b c ;\t ! comment'
    assert str(lp.Entry(' a c ; ')) == 'a c ;'
