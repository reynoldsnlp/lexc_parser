import lexc_parser as lp


def test_parse_entry():
    assert lp.Entry._parse_entry('a:b\t   c         ;\n')   == ['a', ':b', 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a:b\t c ;\n')             == ['a', ':b', 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a:b\t c ;')               == ['a', ':b', 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%::b   c "d"     ;\n')   == ['a%:', ':b', 'c', 'd', None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%::b c "d" ;\n')         == ['a%:', ':b', 'c', 'd', None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%::b c "d" ;')           == ['a%:', ':b', 'c', 'd', None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%%:b   c         ;\n')   == ['a%%', ':b', 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%%:b c ;\n')             == ['a%%', ':b', 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%%:b c ;')               == ['a%%', ':b', 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%%%::b c "d"     ;\n')   == ['a%%%:', ':b', 'c', 'd', None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%%%::b c "d" ;\n')       == ['a%%%:', ':b', 'c', 'd', None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a%%%::b c "d" ;')         == ['a%%%:', ':b', 'c', 'd', None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a       c         ;\n')   == ['a', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a c ;\n')                 == ['a', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a c ;')                   == ['a', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a       c         ;  ')   == ['a', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a c ;  ')                 == ['a', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('a c ;')                   == ['a', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('        c         ;  ')   == [None, None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('c ;  ')                   == [None, None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('c ;')                     == [None, None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('< a b* c+ (d) > c ;\n')   == ['< a b* c+ (d) >', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('< a b* %> c (d) > c ;\n') == ['< a b* %> c (d) >', None, 'c', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('Boris Male ;')            == ['Boris', None, 'Male', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('Vladimir Male ;')         == ['Vladimir', None, 'Male', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('ProperNoun ;')            == [None, None, 'ProperNoun', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('ov Pat ;')                == ['ov', None, 'Pat', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('ic+Msc:ic ProperNoun ;')  == ['ic+Msc', ':ic', 'ProperNoun', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('na+Fem:na ProperNoun ;')  == ['na+Fem', ':na', 'ProperNoun', None, None]  # noqa: E221,E501
    assert lp.Entry._parse_entry('+N+Prop: # ;')            == ['+N+Prop', ':', '#', None, None]  # noqa: E221,E501
