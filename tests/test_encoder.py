#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from textwrap import dedent

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


@mark.parametrize('case', NodeEncoderTestCase.keys())
def test_node_encoder(case):
    data, expected = NodeEncoderTestCase.get(case)
    assert node_encoder(data) == expected


def dump_actual(data):
    text = pureyaml.dump(data)
    print('\n' + text)
    return text


def test_list():
    data = ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']
    expected = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]

    assert dump_actual(data) == expected


def test_dict():
    data = {'name': 'John Smith', 'age': 33}
    expected = dedent("""
        age: 33
        name: John Smith
    """)[1:]

    assert dump_actual(data) == expected


def test_list_of_dicts():
    data = ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']
    expected = dedent("""
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]
    assert dump_actual(data) == expected

@mark.xfail
def test_dict_of_lists():
    data = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on
    expected = dedent("""
        women:
            - Mary Smith
            - Susan Williams
        men:
            - John Smith
            - Bill Jones
    """)[1:]

    assert dump_actual(data) == expected
