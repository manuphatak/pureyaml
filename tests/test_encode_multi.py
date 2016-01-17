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


class EncodeTestCase(MultiTestCaseBase):
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
    it_handles_complex_dict__test_sanity__xfail = None
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
    it_handles_binary__test_pureyaml_sanity__xfail = None
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


def pureyaml_dump(data):
    text = pureyaml.dump(data)
    # print('\n' + text)
    return text


def pyyaml_dump(data):
    text = pyyaml.dump(data, default_flow_style=False)
    # print('\n' + text)
    return text


def encode(data):
    nodes = node_encoder(data)
    return nodes


def sanity(data):
    text = pureyaml.dump(data)
    print(text)
    _data = pureyaml.load(text)
    print(_data)
    return _data


@mark.parametrize('case', EncodeTestCase.keys('encode'))
def test_encode(case):
    data, expected = EncodeTestCase.get('encode', case)
    assert encode(data) == expected


@mark.parametrize('case', EncodeTestCase.keys('pureyaml'))
def test_pureyaml_dump(case):
    data, expected = EncodeTestCase.get('pureyaml', case)
    actual = pureyaml_dump(data)
    print('%s__test_pureyaml_sanity = dedent("""\n%s""")[1:]\n' % (case, actual))
    assert actual == expected


@mark.parametrize('case', EncodeTestCase.keys('sanity'))
def test_sanity(case):
    data, _ = EncodeTestCase.get('sanity', case)
    if case in ['it_handles_simple_nan_float']:
        assert isnan(sanity(data))
        assert isnan(data)
        return
    assert sanity(data) == data


@mark.parametrize('case', EncodeTestCase.keys('pyyaml'))
def test_pyyaml_dump(case):
    data, expected = EncodeTestCase.get('pyyaml', case)
    actual = pyyaml_dump(data)
    print('%s__test_pyyaml = dedent("""\n%s""")[1:]\n' % (case, actual))
    assert actual == expected


# TEST CASE
# ----------------------------------------------------------------------------
def test_it_handles_null__pureyaml_dump():
    data = None
    expected = dedent("""
        null
        ...
    """)[1:]
    actual = pureyaml_dump(data)
    print('expected = dedent("""\n%s""")[1:]\n' % actual)
    assert actual == expected


def test_it_handles_null__pyyaml_dump():
    data = None
    expected = dedent("""
        null
        ...
    """)[1:]
    actual = pyyaml_dump(data)
    print('expected = dedent("""\n%s""")[1:]\n' % actual)
    assert actual == expected


def test_it_handles_null__encode():
    data = None
    expected = Null(None)
    assert encode(data) == expected


def test_it_handles_null__sanity():
    data = None
    assert sanity(data) == data
