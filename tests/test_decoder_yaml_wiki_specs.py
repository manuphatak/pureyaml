#!/usr/bin/env python
# coding=utf-8
"""
source: https://en.wikipedia.org/wiki/YAML#Basic_components_of_YAML
"""
from __future__ import absolute_import

from textwrap import dedent

import yaml as pyyaml
from pytest import mark

import pureyaml
from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import MultiTestCaseBase


class DecoderWikiSpecs(MultiTestCaseBase):
    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_list_block__data = dedent("""
        --- # Favorite movies
            - Casablanca
            - North by Northwest
            - The Man Who Wasn't There
    """)[1:]
    it_can_read_list_block__test_parser = Docs(  # :off
        Doc(
            Sequence(
                Str('Casablanca'),
                Str('North by Northwest'),
                Str("The Man Who Wasn't There"),
            ),
        ),
    )  # :on
    _obj = ['Casablanca', 'North by Northwest', "The Man Who Wasn't There"]
    it_can_read_list_block__test_pureyaml = _obj
    it_can_read_list_block__test_pyyaml = _obj
    it_can_read_list_block__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_list_inline__data = dedent("""
        --- # Shopping list
        [milk, pumpkin pie, eggs, juice]
    """)[1:]
    it_can_read_list_inline__test_parser = Docs(  # :off
        Doc(
            Sequence(
                Str('milk'),
                Str('pumpkin pie'),
                Str('eggs'),
                Str('juice'),
            ),
        ),
    )  # :on
    _obj = ['milk', 'pumpkin pie', 'eggs', 'juice']
    it_can_read_list_inline__test_pureyaml = _obj
    it_can_read_list_inline__test_pyyaml = _obj
    it_can_read_list_inline__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_dict_block__data = dedent("""
        --- # Indented Block
            name: John Smith
            age: 33
    """)[1:]
    it_can_read_dict_block__test_parser = Docs(  # :off
        Doc(
            Map(
                (Str('name'), Str('John Smith')),
                (Str('age'), Int(33)),
            ),
        ),
    )  # :on
    _obj = {'name': 'John Smith', 'age': 33}
    it_can_read_dict_block__test_pureyaml = _obj
    it_can_read_dict_block__test_pyyaml = _obj
    it_can_read_dict_block__test_sanity = None

    it_can_read_dict_inline__data = dedent("""
        {name: John Smith, age: 33}
    """)[1:]
    it_can_read_dict_inline__test_parser = Docs(  # :off
        Doc(
            Map(
                (Str('name'), Str('John Smith')),
                (Str('age'), Int(33)),
            ),
        ),
    )  # :on
    _obj = {'name': 'John Smith', 'age': 33}
    it_can_read_dict_inline__test_pureyaml = _obj
    it_can_read_dict_inline__test_pyyaml = _obj
    it_can_read_dict_inline__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_str_literal__data = dedent("""
        data: |
            There once was a short man from Ealing
            Who got on a bus to Darjeeling
                It said on the door
                "Please don't spit on the floor"
            So he carefully spat on the ceiling
    """)[1:]
    _data = dedent("""
        There once was a short man from Ealing
        Who got on a bus to Darjeeling
            It said on the door
            "Please don't spit on the floor"
        So he carefully spat on the ceiling
    """[1:-1])
    it_can_read_str_literal__test_parser = Docs(  # :off
        Doc(
            Map(
                (
                    Str('data'),
                    Str(_data)
                ),
            ),
        ),
    )  # :on
    _obj = {'data': _data}
    it_can_read_str_literal__test_pureyaml = _obj
    it_can_read_str_literal__test_pyyaml = _obj
    it_can_read_str_literal__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_str_folded__data = dedent("""
        data: >
            Wrapped text
            will be folded
            into a single
            paragraph

            Blank lines denote
            paragraph breaks
    """)[1:]
    _data = (  # :off
        "Wrapped text will be folded into a single paragraph\n"
        "Blank lines denote paragraph breaks\n"
    )  # :on
    it_can_read_str_folded__test_parser = Docs(  # :off
        Doc(
            Map(
                (Str('data'), Str(_data)),
            ),
        ),
    )  # :on
    _obj = {'data': _data}
    it_can_read_str_folded__test_pureyaml = _obj
    it_can_read_str_folded__test_pyyaml = _obj
    it_can_read_str_folded__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_lists_of_dicts__data = dedent("""
        - {name: John Smith, age: 33}
        - name: Mary Smith
          age: 27
    """)[1:]
    it_can_read_lists_of_dicts__test_parser = Docs(  # :off
        Doc(
            Sequence(
                Map(
                    (Str('name'), Str('John Smith')),
                    (Str('age'), Int(33)),
                ),
                Map(
                    (Str('name'), Str('Mary Smith')),
                    (Str('age'), Int(27)),
                ),
            ),
        ),
    )  # :on
    _obj = [  # :off
        {'name': 'John Smith', 'age': 33},
        {'name': 'Mary Smith', 'age': 27}
    ]  # :on
    it_can_read_lists_of_dicts__test_pureyaml = _obj
    it_can_read_lists_of_dicts__test_pyyaml = _obj
    it_can_read_lists_of_dicts__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_dicts_of_lists__data = dedent("""
        men: [John Smith, Bill Jones]
        women:
            - Mary Smith
            - Susan Williams
    """)[1:]
    it_can_read_dicts_of_lists__test_parser = Docs(  # :off
        Doc(
            Map(
                (
                    Str('men'),
                    Sequence(
                        Str('John Smith'),
                        Str('Bill Jones'),
                    ),
                ),
                (
                    Str('women'),
                    Sequence(
                        Str('Mary Smith'),
                        Str('Susan Williams'),
                    ),
                ),
            ),
        ),
    )  # :on
    _obj = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on
    it_can_read_dicts_of_lists__test_pureyaml = _obj
    it_can_read_dicts_of_lists__test_pyyaml = _obj
    it_can_read_dicts_of_lists__test_sanity = None

    # TEST CASE
    # ------------------------------------------------------------------------
    it_can_read_node_anchors_and_references__data = dedent("""
        # sequencer protocols for Laser eye surgery
        ---
        - step:  &id001                  # defines anchor label &id001
            instrument:      Lasik 2000
            pulseEnergy:     5.4
            pulseDuration:   12
            repetition:      1000
            spotSize:        1mm

        - step: &id002
            instrument:      Lasik 2000
            pulseEnergy:     5.0
            pulseDuration:   10
            repetition:      500
            spotSize:        2mm

        - step: *id001                   # refers to the first step (with anchor &id001)
        - step: *id002                   # refers to the second step
        - step: *id001
            spotSize: 2mm                # redefines just this key, refers rest from &id001
        - step: *id002
    """)[1:]
    it_can_read_node_anchors_and_references__test_parser__skip = None
    _obj = [  # :off
        {'step': {
            'instrument': 'Lasik 2000',
            'pulseEnergy': 5.4,
            'pulseDuration': 12,
            'repetition': 1000,
            'spotSize': '1mm',
        }},
        {'step': {
            'instrument': 'Lasik 2000',
            'pulseEnergy': 5.0,
            'pulseDuration': 10,
            'repetition': 500,
            'spotSize': '2mm'

        }},
        {'step': {
            'instrument': 'Lasik 2000',
            'pulseEnergy': 5.4,
            'pulseDuration': 12,
            'repetition': 1000,
            'spotSize': '1mm',
        }},
        {'step': {
            'instrument': 'Lasik 2000',
            'pulseEnergy': 5.0,
            'pulseDuration': 10,
            'repetition': 500,
            'spotSize': '2mm'
        }},
        {'step': {
            'instrument': 'Lasik 2000',
            'pulseEnergy': 5.4,
            'pulseDuration': 12,
            'repetition': 1000,
            'spotSize': '2mm',
        }},
        {'step': {
            'instrument': 'Lasik 2000',
            'pulseEnergy': 5.0,
            'pulseDuration': 10,
            'repetition': 500,
            'spotSize': '2mm'
        }},
    ]  # :on

    it_can_read_node_anchors_and_references__test_pureyaml__skip = _obj
    it_can_read_node_anchors_and_references__test_pyyaml__skip = _obj
    it_can_read_node_anchors_and_references__test_sanity__skip = None

    # TEST CASE
    # ------------------------------------------------------------------------
    _picture = (  # :off
        b"GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee\xe9\xe9"
        b"\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e\x8e\x8e\xe0\xe0"
        b"\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7\x9e\x9e\x9ei^\x10' \x82\n"
        b"\x01\x00;"
    )  # :on
    # noinspection SpellCheckingInspection
    it_can_cast_binary__data = dedent("""
    ---
    picture: !!binary |
        R0lGODlhDAAMAIQAAP//9/X
        17unp5WZmZgAAAOfn515eXv
        Pz7Y6OjuDg4J+fn5OTk6enp
        56enmleECcgggoBADs=mZmE
    """)[1:]
    it_can_cast_binary__test_parser = Docs(  # :off
        Doc(
            Map(
                (Str('picture'), Binary.from_decoded(_picture)),
            ),
        ),
    )  # :on
    _obj = {'picture': _picture}
    it_can_cast_binary__test_pureyaml = _obj
    it_can_cast_binary__test_pyyaml = _obj
    it_can_cast_binary__test_sanity = None


pureyaml_parser = YAMLParser(debug=True)


@mark.parametrize('case', DecoderWikiSpecs.keys('parser'))
def test_parser(case):
    text, expected = DecoderWikiSpecs.get('parser', case)
    nodes = pureyaml_parser.parse(text)
    # print(serialize_nodes(nodes))
    assert nodes == expected


@mark.parametrize('case', DecoderWikiSpecs.keys('pureyaml'))
def test_pureyaml_load(case):
    text, expected = DecoderWikiSpecs.get('pureyaml', case)
    obj = pureyaml.load(text)
    # print('{case}__test_pureyaml = {obj!r}'.format(case=case, obj=obj))
    assert obj == expected


@mark.parametrize('case', DecoderWikiSpecs.keys('pyyaml'))
def test_pyyaml_load(case):
    text, expected = DecoderWikiSpecs.get('pyyaml', case)
    obj = pyyaml.load(text)
    # print('{case}__test_pyyaml = {obj!r}'.format(case=case, obj=obj))
    assert obj == expected


@mark.parametrize('case', DecoderWikiSpecs.keys('sanity'))
def test_sanity(case):
    text, _ = DecoderWikiSpecs.get('sanity', case)
    obj1 = pureyaml.load(text)
    # print(obj1)
    _text = pureyaml.dump(obj1)
    # print(_text)
    obj2 = pureyaml.load(_text)
    # print(obj2)
    assert obj1 == obj2


casted_data_types = """
---
a: 123                     # an integer
b: "123"                   # a string, disambiguated by quotes
c: 123.0                   # a float
d: !!float 123             # also a float via explicit data type prefixed by (!!)
e: !!str 123               # a string, disambiguated by explicit type
f: !!str Yes               # a string via explicit type
g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
h: Yes we have No bananas  # a string, "Yes" and "No" disambiguated by context.
"""

casted_data_type_args = [  # :off
    ('a', int),
    ('b', str),
    ('c', float),
    ('d', float),
    ('e', str),
    ('f', str),
    ('g', bool),
    ('h', str)
]  # :on


@mark.parametrize('key,type_', casted_data_type_args)
def test_can_read_casted_data_types(key, type_):
    obj = pureyaml.load(casted_data_types)
    assert isinstance(obj[key], type_)


def test_can_read_values_from_casted_data__str_from_int():
    obj = pureyaml.load(casted_data_types)
    assert obj['e'] == '123'


def test_can_read_values_from_casted_data__str_from_keyword():
    obj = pureyaml.load(casted_data_types)
    assert obj['f'] == 'Yes'


def test_can_read_values_from_casted_data__bool():
    obj = pureyaml.load(casted_data_types)
    assert obj['g'] is True


def test_can_read_values_from_casted_data__str_from_context():
    obj = pureyaml.load(casted_data_types)
    assert obj['h'] == 'Yes we have No bananas'
