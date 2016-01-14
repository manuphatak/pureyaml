#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from textwrap import dedent

from future.utils import PYPY, PY2
from pytest import mark

import pureyaml
from pureyaml.encoder import node_encoder
from pureyaml.nodes import *  # noqa
from tests.utils import ParametrizedTestData, PY34, PY35


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
            b"GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee\xe9"
            b"\xe9\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e\x8e\x8e"
            b"\xe0\xe0\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7\x9e\x9e\x9ei^"
            b"\x10' \x82\n\x01\x00;"
        )  # :on
    }
    # noinspection SpellCheckingInspection
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


def test_node_binary_encoder():
    data, expected = NodeEncoderTestCase.get('test_binary')

    picture = (  # :off
        b"GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee\xe9"
        b"\xe9\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e\x8e\x8e"
        b"\xe0\xe0\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7\x9e\x9e\x9ei^"
        b"\x10' \x82\n\x01\x00;"
    )  # :on
    encoded_nodes = node_encoder(data)
    picture_actual = encoded_nodes.value[0][1].value
    assert picture_actual == picture


def dump(data):
    text = pureyaml.dump(data)
    # print('\n' + text)
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


def test_dump__lists_of_dicts():
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


def test_dump__dict_of_lists():
    data = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on

    if PY34 or PY35:
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
    if PY34 or PY35:
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
    data = [  # :off
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
    if PY34 or PY35:
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


def test_dump__casted_data():
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
    if PY34 or PY35:
        expected = dedent("""
            g: true
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
            g: true
            h: Yes we have No bananas
        """)[1:]
    else:
        expected = dedent("""
            a: 123
            c: 123.0
            b: '123'
            e: '123'
            d: 123.0
            g: true
            f: 'Yes'
            h: Yes we have No bananas
        """)[1:]
    actual = dump(data)

    assert actual == expected


def test_dump__travis_yaml():
    # noinspection SpellCheckingInspection
    secure_block = (  # :off
        'ndFpfTvPZN8SfvduvS4567k1TqYl7L7lRxxEPjmRzg3OgzMgCHRMO/uCrce5i8TkxTWL'
        'W82ArNvBZnTkRzGyChKfoNzKwukgrJACOibc6cPgNBPpuDpZTb7X6hZixSs9VBsMwL9T'
        'kQfImq3Q2uSnW7tBrHYKEIOXeCmKzomI3RYxWoxOlrAP7TqUjxyw/Ax5pOdjODDEMOjB'
        'Z8qRcrRD/n/JyAQrNVtaEaMkauTPbvJ86vG8mDPLzD3c2PFK1qAOimcJb5izM9y9kent'
        '/muLfjeruBxwYGrqAkQnWM0KUqMbfZ9sxMO0hgMZs3p2fldTyANC9bRu65XLW3qseHs9'
        'NTbbdgAZMlsXU9WxzvxTyibvMGHODyps/Ra9NkgRZJC9NLsabuw42P3AVfQjhih/dwn0'
        'DjRU+DlNyY291CazPjSWP4hLBAp72hhv1sGQD33sY3ERx5XPXyeb1B32s3l94bpdPwzO'
        'Hf3MIHAs4Uj32mToi0699lp749PQ4o0Jb2WF0P8vh+vlOJNVM+51vO5CmEj2cF7rJcrb'
        'n+T68gmlvqcYCt3q5gCn+4iBhzGCqeDxlDU1jgC9T/9V4Q+qyAEv/wtYDduoe4R1WGWO'
        'lqSxr8k6Tr92CjI1TXbJUP3N3V0pNYayUJDIIvjWy7T/10xRhMaRhBM88XDJh7QBpcZT'
        'KJo='
    )  # :on
    data = {  # :off
        'env': [
            'TOXENV=py26',
            'TOXENV=py27',
            'TOXENV=py33',
            'TOXENV=py34',
            'TOXENV=py35',
            'TOXENV=pypy',
            'TOXENV=docs'
        ],
        'language': 'python',
        'script': ['tox -e $TOXENV'],
        'python': ['3.5'],
        'after_success': ['coveralls'],
        'install': ['pip install tox coveralls'],
        'deploy': {
            True: {
                'repo': 'bionikspoon/pureyaml',
                'condition': '$TOXENV == py34',
                'tags': True
            },
            'password': {
                'secure': secure_block
            },
            'distributions': 'sdist bdist_wheel',
            'user': 'bionikspoon',
            'provider': 'pypi'
        }
    }  # :on
    if PY34 or PY35:
        expected = dedent("""
            python:
            - '3.5'
            after_success:
            - coveralls
            install:
            - pip install tox coveralls
            env:
            - TOXENV=py26
            - TOXENV=py27
            - TOXENV=py33
            - TOXENV=py34
            - TOXENV=py35
            - TOXENV=pypy
            - TOXENV=docs
            script:
            - tox -e $TOXENV
            deploy:
              true:
                condition: $TOXENV == py34
                tags: true
                repo: bionikspoon/pureyaml
              provider: pypi
              distributions: sdist bdist_wheel
              password:
                secure: {secure_block}
              user: bionikspoon
            language: python
        """)[1:].format(secure_block=secure_block)
    elif PY2:
        expected = dedent("""
            env:
            - TOXENV=py26
            - TOXENV=py27
            - TOXENV=py33
            - TOXENV=py34
            - TOXENV=py35
            - TOXENV=pypy
            - TOXENV=docs
            language: python
            script:
            - tox -e $TOXENV
            python:
            - '3.5'
            after_success:
            - coveralls
            install:
            - pip install tox coveralls
            deploy:
              true:
                repo: bionikspoon/pureyaml
                condition: $TOXENV == py34
                tags: true
              password:
                secure: {secure_block}
              distributions: sdist bdist_wheel
              user: bionikspoon
              provider: pypi
        """)[1:].format(secure_block=secure_block)
    else:
        expected = dedent("""
            install:
            - pip install tox coveralls
            env:
            - TOXENV=py26
            - TOXENV=py27
            - TOXENV=py33
            - TOXENV=py34
            - TOXENV=py35
            - TOXENV=pypy
            - TOXENV=docs
            language: python
            script:
            - tox -e $TOXENV
            python:
            - '3.5'
            after_success:
            - coveralls
            deploy:
              true:
                repo: bionikspoon/pureyaml
                condition: $TOXENV == py34
                tags: true
              password:
                secure: {secure_block}
              distributions: sdist bdist_wheel
              user: bionikspoon
              provider: pypi
        """)[1:].format(secure_block=secure_block)

    actual = dump(data)
    assert actual == expected
