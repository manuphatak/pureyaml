#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from textwrap import dedent

from future.utils import PY3, PYPY
from pytest import mark

import pureyaml
from pureyaml.encoder import node_encoder
from pureyaml.nodes import *  # noqa
from tests.utils import ParametrizedTestData


class NodeEncoderTestCase(ParametrizedTestData):
    test_int = 1, Int(1)
    test_str = '1', Str(1)
    test_null = None, Null(None)
    test_float__implicit = 1., Float(1)
    test_float__explicit = float(1), Float(1)
    test_float__nan = float('nan'), Float('nan')
    test_float__inf = float('-inf'), Float('-inf')
    test_bool = True, Bool(True)
    test_list__int = [1, 2, 3], Sequence(Int(1), Int(2), Int(3))
    test_list__list__int = (  # :off
        [[1, 2], [3], [4, 5, 6]],
        Sequence(
            Sequence(Int(1), Int(2)),
            Sequence(Int(3)),
            Sequence(Int(4), Int(5), Int(6)),
        )
    )  # :on
    test_dict__int = {'1': 1}, Map((Str(1), Int(1)))

    test_dict__dict_complex__data = {  # :off
        '1': {'2': 3},
        '4': {5: [
            {'6': [7, 8]},
            {'9': 10}
        ]}
    }  # :on
    test_dict__dict_complex__expected = Map(  # :off
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

    test_binary__data = {
        'picture': (  # :off
            "GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee\xe9"
            "\xe9\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e\x8e\x8e"
            "\xe0\xe0\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7\x9e\x9e\x9ei^"
            "\x10' \x82\n\x01\x00;"
        )  # :on
    }
    test_binary__expected = Map(  # :off
        (
            Str('picture'),
            Binary(
                b'R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5OTk6enp56enmle\n'
                b'ECcgggoBADs=\n'
            )
        )
    )  # :on


@mark.parametrize('case', NodeEncoderTestCase.keys())
def test_node_encoder(case):
    data, expected = NodeEncoderTestCase.get(case)
    assert node_encoder(data) == expected


def dump(data):
    text = pureyaml.dump(data)
    print('\n' + text)
    return text


def test_dump__list():
    data = ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']
    expected = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]

    assert dump(data) == expected


def test_dump__dict():
    data = {'name': 'John Smith', 'age': 33}
    if not PYPY:
        expected = dedent("""
            age: 33
            name: John Smith
        """)[1:]
    else:
        expected = dedent("""
            name: John Smith
            age: 33
        """)[1:]

    assert dump(data) == expected


def test_dump__list_of_dicts():
    data = ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']
    expected = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]
    assert dump(data) == expected


def test_dump__dict_of_lists():
    data = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on
    if PY3:
        expected = dedent("""
            women:
              - Mary Smith
              - Susan Williams
            men:
              - John Smith
              - Bill Jones
        """)[1:]
    else:
        expected = dedent("""
            men:
              - John Smith
              - Bill Jones
            women:
              - Mary Smith
              - Susan Williams
        """)[1:]
    assert dump(data) == expected


def test_dump__nested_obj():
    data = {  # :off
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
    if PY3:
        expected = dedent("""
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
    elif PYPY:
        expected = dedent("""
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
    else:
        expected = dedent("""
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

    assert dump(data) == expected


def test_dump__nested_list():
    data = [1,  # :off
            [[2,
              3],
             [4,
              [5,
               6]],
             7],
            [8,
             9,
             10],
            [[11, 12],
             [13, 14, 15, 16]]]  # :on
    expected = dedent("""
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

    assert dump(data) == expected


def test_dump__complex_mixed_obj():
    data = {  # :off
        '1': {'2': 3},
        '4': {5: [
            {'6': [7, 8], 9: '10', 11: '12'},
            {'13': 14}
        ]}
    }  # :on
    if PY3:
        expected = dedent("""
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
    elif PYPY:
        expected = dedent("""
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
    else:
        expected = dedent("""
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

    assert dump(data) == expected


def test_dump__list__alt():
    data = ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']
    expected = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]

    assert dump(data) == expected


def test_dump__dict__alt():
    data = {'name': 'John Smith', 'age': 33}
    if not PYPY:
        expected = dedent("""
            age: 33
            name: John Smith
        """)[1:]
    else:
        expected = dedent("""
            name: John Smith
            age: 33
        """)[1:]

    assert dump(data) == expected


def test_dump__lists_of_dicts__alt():
    data = [  # :off
        {'name': 'John Smith', 'age': 33},
        {'name': 'Mary Smith', 'age': 27}
    ]  # :on
    if not PYPY:
        expected = dedent("""
            - age: 33
              name: John Smith
            - age: 27
              name: Mary Smith
        """)[1:]
    else:
        expected = dedent("""
            - name: John Smith
              age: 33
            - name: Mary Smith
              age: 27
        """)[1:]
    assert dump(data) == expected


def test_dump__dicts_of_lists__alt():
    data = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on
    if PY3:
        expected = dedent("""
            women:
              - Mary Smith
              - Susan Williams
            men:
              - John Smith
              - Bill Jones
        """)[1:]
    else:
        expected = dedent("""
            men:
              - John Smith
              - Bill Jones
            women:
              - Mary Smith
              - Susan Williams
        """)[1:]
    assert dump(data) == expected


def test_dump__casted_data__alt():
    data = {  # :off
        'a': 123,
        'b': str(123),
        'c': 123.0,
        'd': float(123),
        'e': str(123),
        'f': 'Yes',
        'g': True,
        'h': 'Yes we have No bananas',
    }  # :on
    if PY3:
        expected = dedent("""
            g: True
            b: '123'
            h: Yes we have No bananas
            c: 123.0
            e: '123'
            a: 123
            f: 'Yes'
            d: 123.0
        """)[1:]
    elif PYPY:
        expected = dedent("""
            a: 123
            b: '123'
            c: 123.0
            d: 123.0
            e: '123'
            f: 'Yes'
            g: True
            h: Yes we have No bananas
        """)[1:]
    else:
        expected = dedent("""
            a: 123
            c: 123.0
            b: '123'
            e: '123'
            d: 123.0
            g: True
            f: 'Yes'
            h: Yes we have No bananas
        """)[1:]

    assert dump(data) == expected
