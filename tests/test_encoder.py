#!/usr/bin/env python
# coding=utf-8
from math import isnan
from textwrap import dedent

import yaml as pyyaml
from pytest import mark

import pureyaml
from pureyaml.encoder import node_encoder
from pureyaml.nodes import *  # noqa
from tests.utils import MultiTestCaseBase


class EncoderTestCase(MultiTestCaseBase):
    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_int__data = 1
    it_handles_simple_int__test_pyyaml = dedent("""
        1
        ...
    """)[1:]
    it_handles_simple_int__test_pureyaml_sanity = dedent("""
        1
        ...
    """)[1:]
    it_handles_simple_int__test_encode = Int(1)

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_str__data = '1'
    it_handles_simple_str__test_pyyaml = dedent("""
        '1'
    """)[1:]
    it_handles_simple_str__test_pureyaml_sanity = dedent("""
        '1'
    """)[1:]
    it_handles_simple_str__test_encode = Str(1)

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_implicit_float__data = 1.
    it_handles_simple_implicit_float__test_pyyaml = dedent("""
        1.0
        ...
    """)[1:]
    it_handles_simple_implicit_float__test_pureyaml_sanity = dedent("""
        1.0
        ...
    """)[1:]
    it_handles_simple_implicit_float__test_encode = Float(1)

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_explicit_float__data = float(1)
    it_handles_simple_explicit_float__test_pyyaml = dedent("""
        1.0
        ...
    """)[1:]
    it_handles_simple_explicit_float__test_pureyaml_sanity = dedent("""
        1.0
        ...
    """)[1:]
    it_handles_simple_explicit_float__test_encode = Float(1)

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_nan_float__data = float('nan')
    it_handles_simple_nan_float__test_pyyaml = dedent("""
        .nan
        ...
    """)[1:]
    it_handles_simple_nan_float__test_pureyaml_sanity = dedent("""
        .nan
        ...
    """)[1:]
    it_handles_simple_nan_float__test_encode = Float('nan')

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_inf_float__data = float('-inf')
    it_handles_simple_inf_float__test_pyyaml = dedent("""
        -.inf
        ...
    """)[1:]
    it_handles_simple_inf_float__test_pureyaml_sanity = dedent("""
        -.inf
        ...
    """)[1:]
    it_handles_simple_inf_float__test_encode = Float('-inf')

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_bool__data = True
    it_handles_simple_bool__test_pyyaml = dedent("""
        true
        ...
    """)[1:]
    it_handles_simple_bool__test_pureyaml_sanity = dedent("""
        true
        ...
    """)[1:]
    it_handles_simple_bool__test_encode = Bool(True)

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_list__data = [1, 2, 3]
    it_handles_simple_list__test_pyyaml = dedent("""
        - 1
        - 2
        - 3
    """)[1:]
    it_handles_simple_list__test_pureyaml_sanity = dedent("""
        - 1
        - 2
        - 3
    """)[1:]
    it_handles_simple_list__test_encode = Sequence(Int(1), Int(2), Int(3))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_lists_of_list__data = [[1, 2], [3], [4, 5, 6]]

    it_handles_lists_of_list__test_pyyaml = dedent("""
        - - 1
          - 2
        - - 3
        - - 4
          - 5
          - 6
    """)[1:]
    it_handles_lists_of_list__test_pureyaml_sanity = dedent("""
        - - 1
          - 2
        - - 3
        - - 4
          - 5
          - 6
    """)[1:]
    it_handles_lists_of_list__test_encode = Sequence(  # :off
        Sequence(Int(1), Int(2)),
        Sequence(Int(3)),
        Sequence(Int(4), Int(5), Int(6)),
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_simple_dict__data = {'1': 1}
    it_handles_simple_dict__test_pyyaml = dedent("""
        '1': 1
    """)[1:]
    it_handles_simple_dict__test_pureyaml_sanity = dedent("""
        '1': 1
    """)[1:]
    it_handles_simple_dict__test_encode = Map((Str(1), Int(1)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_complex_dict__data = {  # :off
        '1': {
            '2': 3
        },
        '4': {
            5: [
                {
                    '6': [7, 8]
                },
                {'9': 10}
            ]
        }
    }  # :on
    it_handles_complex_dict__test_pyyaml = dedent("""
        '1':
          '2': 3
        '4':
          5:
          - '6':
            - 7
            - 8
          - '9': 10
    """)[1:]
    it_handles_complex_dict__test_pureyaml__PY34__PY35 = dedent("""
        '4':
          5:
          - '6':
            - 7
            - 8
          - '9': 10
        '1':
          '2': 3
    """)[1:]
    it_handles_complex_dict__test_pureyaml__PY2__PY33 = dedent("""
        '1':
          '2': 3
        '4':
          5:
          - '6':
            - 7
            - 8
          - '9': 10
    """)[1:]
    it_handles_complex_dict__test_sanity = None
    it_handles_complex_dict__test_encode = Map(  # :off
        (
            Str(1),
            Map(
                (Str(2), Int(3))
            )
        ),
        (
            Str(4),
            Map(
                (
                    Int(5),
                    Sequence(
                        Map(
                            (
                                Str(6),
                                Sequence(
                                    Int(7),
                                    Int(8),
                                )
                            )
                        ),
                        Map(
                            (Str(9), Int(10))
                        )
                    )
                )
            )
        )
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_binary__data = {
        'picture': (  # :off
            b"GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee\xe9"
            b"\xe9\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e\x8e\x8e"
            b"\xe0\xe0\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7\x9e\x9e\x9ei^"
            b"\x10' \x82\n\x01\x00;"
        )  # :on
    }
    # noinspection SpellCheckingInspection
    it_handles_binary__test_pyyaml = dedent("""
        picture: !!binary |
          R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5OTk6enp56enmle
          ECcgggoBADs=
    """)[1:]
    # noinspection SpellCheckingInspection
    it_handles_binary__test_pureyaml = dedent("""
        picture: !!binary |
          R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5OTk6enp56enmleECcgggoBADs=
    """)[1:]
    it_handles_binary__test_sanity = None
    # noinspection SpellCheckingInspection
    it_handles_binary__test_encode = Map(  # :off
        (
            Str('picture'),
            Binary(
                b'R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J'
                b'+fn5OTk6enp56enmle\n'
                b'ECcgggoBADs=\n'
            )
        )
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_dict__data = {'name': 'John Smith', 'age': 33}
    it_handles_dict__test_pureyaml_sanity__not_PYPY = dedent("""
        age: 33
        name: John Smith
    """)[1:]
    it_handles_dict__test_pureyaml_sanity__PYPY = dedent("""
        name: John Smith
        age: 33
    """)[1:]
    it_handles_dict__test_pyyaml = dedent("""
        age: 33
        name: John Smith
    """)[1:]
    it_handles_dict__test_encode = Map(  # :off
        (Str('name'), Str('John Smith')),
        (Str('age'), Int(33)),
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_list__data = ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']
    it_handles_list__test_encode = Sequence(  # :off
        Str('Casablanca'),
        Str('North by Northwest'),
        Str("The Man Who Wasn't There"),
    )  # :on
    it_handles_list__test_pureyaml = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]
    it_handles_list__test_pyyaml = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]
    it_handles_list__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_lists_of_dicts__data = [  # :off
        {'name': 'John Smith', 'age': 33},
        {'name': 'Mary Smith', 'age': 27}
    ]  # :on
    it_handles_lists_of_dicts__test_encode = Sequence(  # :off
        Map(
            (Str('name'), Str('John Smith')),
            (Str('age'), Int(33)),
        ),
        Map(
            (Str('name'), Str('Mary Smith')),
            (Str('age'), Int(27)),
        ),
    )  # :on
    it_handles_lists_of_dicts__test_pureyaml__not_PYPY = dedent("""
        - age: 33
          name: John Smith
        - age: 27
          name: Mary Smith
    """)[1:]
    it_handles_lists_of_dicts__test_pureyaml__PYPY = dedent("""
        - name: John Smith
          age: 33
        - name: Mary Smith
          age: 27
    """)[1:]
    it_handles_lists_of_dicts__test_pyyaml = dedent("""
        - age: 33
          name: John Smith
        - age: 27
          name: Mary Smith
    """)[1:]
    it_handles_lists_of_dicts__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_dict_of_lists__data = {  # :off
            'men': ['John Smith', 'Bill Jones'],
            'women': ['Mary Smith', 'Susan Williams']
        }  # :on
    it_handles_dict_of_lists__test_encode = Map(  # :off
        (
            Str('men'),
            Sequence(
                Str('John Smith'),
                Str('Bill Jones'),
            )
        ),
        (
            Str('women'),
            Sequence(
                Str('Mary Smith'),
                Str('Susan Williams'),
            )
        ),
    )  # :on
    it_handles_dict_of_lists__test_pureyaml__PY34__PY35 = dedent("""
        women:
        - Mary Smith
        - Susan Williams
        men:
        - John Smith
        - Bill Jones
    """)[1:]
    it_handles_dict_of_lists__test_pureyaml__PY2__PY33 = dedent("""
        men:
        - John Smith
        - Bill Jones
        women:
        - Mary Smith
        - Susan Williams
    """)[1:]
    it_handles_dict_of_lists__test_pyyaml = dedent("""
        men:
        - John Smith
        - Bill Jones
        women:
        - Mary Smith
        - Susan Williams
    """)[1:]
    it_handles_dict_of_lists__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_nested_obj__data = {  # :off
        '1': {
            '2': 3
        },
        '4': {
            5: {
                '6': 7,
                '8': 9,
                '10': 11,
                '12': {
                    '13': {
                        '14': '15'
                    }
                }
            },
            16: 17
        }
    }  # :on
    it_handles_nested_obj__test_encode = Map(  # :off
        (
            Str('1'),
            Map(
                (Str('2'), Int(3)),
            )
        ),
        (
            Str('4'),
            Map(
                (
                    Int(5),
                    Map(
                        (Str('6'), Int(7)),
                        (Str('8'), Int(9)),
                        (Str('10'), Int(11)),
                        (
                            Str('12'),
                            Map(
                                (
                                    Str('13'),
                                    Map(
                                        (Str('14'), Str('15')),
                                    )
                                ),
                            )
                        ),
                    )
                ),
                (Int(16), Int(17)),
            )
        ),
    )  # :on
    it_handles_nested_obj__test_pureyaml__PY34__PY34 = dedent("""
        '4':
          16: 17
          5:
            '10': 11
            '12':
              '13':
                '14': '15'
            '8': 9
            '6': 7
        '1':
          '2': 3
    """)[1:]
    it_handles_nested_obj__test_pureyaml__PYPY = dedent("""
        '1':
          '2': 3
        '4':
          5:
            '6': 7
            '8': 9
            '10': 11
            '12':
              '13':
                '14': '15'
          16: 17
    """)[1:]
    it_handles_nested_obj__test_pureyaml__PY26__PY27__PY33 = dedent("""
        '1':
          '2': 3
        '4':
          16: 17
          5:
            '8': 9
            '12':
              '13':
                '14': '15'
            '10': 11
            '6': 7
    """)[1:]
    it_handles_nested_obj__test_pyyaml = dedent("""
        '1':
          '2': 3
        '4':
          5:
            '10': 11
            '12':
              '13':
                '14': '15'
            '6': 7
            '8': 9
          16: 17
    """)[1:]
    it_handles_nested_obj__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_nested_list__data = [  # :off
            1,
            [
                [
                    2,
                    3
                ],
                [
                    4,
                    [
                        5,
                        6
                    ]
                ],
                7
            ],
            [
                8,
                9,
                10
            ],
            [
                [
                    11,
                    12
                ],
                [
                    13,
                    14,
                    15,
                    16
                ]
            ]
        ]  # :on
    it_handles_nested_list__test_encode = Sequence(  # :off
        Int(1),
        Sequence(
            Sequence(
                Int(2),
                Int(3),
            ),
            Sequence(
                Int(4),
                Sequence(
                    Int(5),
                    Int(6),
                ),
            ),
            Int(7),
        ),
        Sequence(
            Int(8),
            Int(9),
            Int(10),
        ),
        Sequence(
            Sequence(
                Int(11),
                Int(12),
            ),
            Sequence(
                Int(13),
                Int(14),
                Int(15),
                Int(16),
            ),
        ),
    )  # :on
    it_handles_nested_list__test_pureyaml = dedent("""
        - 1
        - - - 2
            - 3
          - - 4
            - - 5
              - 6
          - 7
        - - 8
          - 9
          - 10
        - - - 11
            - 12
          - - 13
            - 14
            - 15
            - 16
    """)[1:]
    it_handles_nested_list__test_pyyaml = dedent("""
        - 1
        - - - 2
            - 3
          - - 4
            - - 5
              - 6
          - 7
        - - 8
          - 9
          - 10
        - - - 11
            - 12
          - - 13
            - 14
            - 15
            - 16
    """)[1:]
    it_handles_nested_list__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_complex_mixed_obj__data = {  # :off
        '1': {'2': 3},
        '4': {5: [
            {'6': [7, 8], 9: '10', 11: '12'},
            {'13': 14}
        ]}
    }  # :on
    it_handles_complex_mixed_obj__test_encode = Map(  # :off
        (
            Str('1'),
            Map(
                (Str('2'), Int(3)),
            )
        ),
        (
            Str('4'),
            Map(
                (
                    Int(5),
                    Sequence(
                        Map(
                            (
                                Str('6'),
                                Sequence(
                                    Int(7),
                                    Int(8),
                                ),
                            ),
                            (Int(9), Str('10')),
                            (Int(11), Str('12')),
                        ),
                        Map(
                            (Str('13'), Int(14)),
                        ),
                    )
                ),
            )
        ),
    )  # :on
    it_handles_complex_mixed_obj__test_pureyaml__PY34__PY34 = dedent("""
        '4':
          5:
          - 9: '10'
            11: '12'
            '6':
            - 7
            - 8
          - '13': 14
        '1':
          '2': 3
    """)[1:]
    it_handles_complex_mixed_obj__test_pureyaml__PYPY = dedent("""
        '1':
          '2': 3
        '4':
          5:
          - '6':
            - 7
            - 8
            9: '10'
            11: '12'
          - '13': 14
    """)[1:]
    it_handles_complex_mixed_obj__test_pureyaml__PY26__PY27__PY33 = dedent("""
        '1':
          '2': 3
        '4':
          5:
          - 9: '10'
            11: '12'
            '6':
            - 7
            - 8
          - '13': 14
    """)[1:]
    it_handles_complex_mixed_obj__test_pyyaml = dedent("""
        '1':
          '2': 3
        '4':
          5:
          - 9: '10'
            11: '12'
            '6':
            - 7
            - 8
          - '13': 14
    """)[1:]
    it_handles_complex_mixed_obj__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casted_data__data = {  # :off
        'a': 123,
        'b': str(123),
        'c': 123.0,
        'd': float(123),
        'e': str(123),
        'f': 'Yes',
        'g': True,
        'h': 'Yes we have No bananas',
    }  # :on
    it_handles_casted_data__test_encode = Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str('123')),
        (Str('c'), Float(123.0)),
        (Str('d'), Float(123.0)),
        (Str('e'), Str('123')),
        (Str('f'), Str('Yes')),
        (Str('g'), Bool(True)),
        (Str('h'), Str('Yes we have No bananas')),
    )  # :on
    it_handles_casted_data__test_pureyaml__PY34__PY35 = dedent("""
        g: true
        b: '123'
        h: Yes we have No bananas
        c: 123.0
        e: '123'
        a: 123
        f: 'Yes'
        d: 123.0
    """)[1:]
    it_handles_casted_data__test_pureyaml__PYPY = dedent("""
        a: 123
        b: '123'
        c: 123.0
        d: 123.0
        e: '123'
        f: 'Yes'
        g: true
        h: Yes we have No bananas
    """)[1:]
    it_handles_casted_data__test_pureyaml__PY26__PY27__PY33 = dedent("""
        a: 123
        c: 123.0
        b: '123'
        e: '123'
        d: 123.0
        g: true
        f: 'Yes'
        h: Yes we have No bananas
    """)[1:]
    it_handles_casted_data__test_pyyaml = dedent("""
        a: 123
        b: '123'
        c: 123.0
        d: 123.0
        e: '123'
        f: 'Yes'
        g: true
        h: Yes we have No bananas
    """)[1:]
    it_handles_casted_data__test_sanity = None


@mark.parametrize('case', EncoderTestCase.keys('encode'))
def test_encode(case):
    obj, expected = EncoderTestCase.get('encode', case)
    nodes = node_encoder(obj)
    # print(serialize_nodes(nodes))
    assert nodes == expected


@mark.parametrize('case', EncoderTestCase.keys('pureyaml'))
def test_pureyaml_dump(case):
    obj, expected = EncoderTestCase.get('pureyaml', case)
    text = pureyaml.dump(obj)
    # print('%s__test_pureyaml_sanity = dedent("""\n%s""")[1:]\n' % (case, text))
    assert text == expected


@mark.parametrize('case', EncoderTestCase.keys('sanity'))
def test_sanity(case):
    obj1, _ = EncoderTestCase.get('sanity', case)
    # print(obj1)
    text = pureyaml.dump(obj1)
    # print(text)
    obj2 = pureyaml.load(text)
    # print(obj2)
    if case in ['it_handles_simple_nan_float']:
        assert isnan(obj2)
        assert isnan(obj1)
        return

    assert obj2 == obj1


def pyyaml_dump(obj):
    text = pyyaml.dump(obj, default_flow_style=False)
    return text


@mark.parametrize('case', EncoderTestCase.keys('pyyaml'))
def test_pyyaml_dump(case):
    obj, expected = EncoderTestCase.get('pyyaml', case)
    text = pyyaml_dump(obj)
    # print('%s__test_pyyaml = dedent("""\n%s""")[1:]\n' % (case, text))
    assert text == expected


# TEST CASE
# ----------------------------------------------------------------------------
def test_it_handles_null__pureyaml_dump():
    obj = None
    expected = dedent("""
        null
        ...
    """)[1:]
    text = pureyaml.dump(obj)
    assert text == expected


def test_it_handles_null__pyyaml_dump():
    obj = None
    expected = dedent("""
        null
        ...
    """)[1:]
    text = pyyaml_dump(obj)
    assert text == expected


def test_it_handles_null__encode():
    obj = None
    expected = Null(None)
    nodes = node_encoder(obj)
    assert nodes == expected


def test_it_handles_null__sanity():
    obj1 = None
    # print(obj1)
    text = pureyaml.dump(obj1)
    # print(text)
    obj2 = pureyaml.load(text)
    # print(obj2)

    assert obj2 == obj1
