#!/usr/bin/env python
# coding=utf-8
"""
source: https://en.wikipedia.org/wiki/YAML#Basic_components_of_YAML
"""
from base64 import standard_b64decode
from textwrap import dedent

from pytest import mark

import pureyaml

list_block = """
--- # Favorite movies
    - Casablanca
    - North by Northwest
    - The Man Who Wasn't There
"""


def test_can_read_list_block():
    result = pureyaml.load(list_block)

    assert result == ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']


list_inline = """
--- # Shopping list
[milk, pumpkin pie, eggs, juice]
"""


def test_can_read_list_inline():
    result = pureyaml.load(list_inline)

    assert result == ['milk', 'pumpkin pie', 'eggs', 'juice']


dict_block = """
--- # Indented Block
    name: John Smith
    age: 33
"""


def test_can_read_dict_block():
    result = pureyaml.load(dict_block)
    expected = {'name': 'John Smith', 'age': 33}

    assert result == expected


dict_inline = """
{name: John Smith, age: 33}
"""


def test_can_read_dict_inline():
    result = pureyaml.load(dict_inline)
    expected = {'name': 'John Smith', 'age': 33}

    assert result == expected


str_literal = """
data: |
    There once was a short man from Ealing
    Who got on a bus to Darjeeling
        It said on the door
        "Please don't spit on the floor"
    So he carefully spat on the ceiling
"""


def test_can_read_str_literal():
    result = pureyaml.load(str_literal)
    data = dedent("""
        There once was a short man from Ealing
        Who got on a bus to Darjeeling
            It said on the door
            "Please don't spit on the floor"
        So he carefully spat on the ceiling
        """[1:-1])

    expected = {'data': data}

    assert result == expected


str_folded = """
data: >
    Wrapped text
    will be folded
    into a single
    paragraph

    Blank lines denote
    paragraph breaks
"""


def test_can_read_str_folded():
    result = pureyaml.load(str_folded)
    data = "Wrapped text will be folded into a single paragraph\nBlank lines denote paragraph breaks\n"

    expected = {'data': data}
    assert result == expected


lists_of_dicts = """
- {name: John Smith, age: 33}
- name: Mary Smith
  age: 27
"""


def test_can_read_lists_of_dicts():
    result = pureyaml.load(lists_of_dicts)
    expected = [  # :off
        {'name': 'John Smith', 'age': 33},
        {'name': 'Mary Smith', 'age': 27}
    ]  # :on

    assert result == expected


dicts_of_lists = """
men: [John Smith, Bill Jones]
women:
    - Mary Smith
    - Susan Williams
"""


def test_can_read_dicts_of_lists():
    result = pureyaml.load(dicts_of_lists)
    expected = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on

    assert result == expected


node_anchors_and_references = """
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
"""


@mark.xfail(reason='References not supported')
def test_can_read_node_anchors_and_references():
    result = pureyaml.load(node_anchors_and_references)
    expected = [  # :off
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

    assert result == expected


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
    data = pureyaml.load(casted_data_types)
    assert isinstance(data[key], type_)


def test_can_read_values_from_casted_data__str_from_int():
    data = pureyaml.load(casted_data_types)
    assert data['e'] == '123'


def test_can_read_values_from_casted_data__str_from_keyword():
    data = pureyaml.load(casted_data_types)
    assert data['f'] == 'Yes'


def test_can_read_values_from_casted_data__bool():
    data = pureyaml.load(casted_data_types)
    assert data['g'] is True


def test_can_read_values_from_casted_data__str_from_context():
    data = pureyaml.load(casted_data_types)
    assert data['h'] == 'Yes we have No bananas'


# noinspection SpellCheckingInspection
specified_data_types__binary = """
---
picture: !!binary |
    R0lGODlhDAAMAIQAAP//9/X
    17unp5WZmZgAAAOfn515eXv
    Pz7Y6OjuDg4J+fn5OTk6enp
    56enmleECcgggoBADs=mZmE
"""


def test_can_read_specified_data_types__binary():
    result = pureyaml.load(specified_data_types__binary)
    # noinspection SpellCheckingInspection
    picture = standard_b64decode(dedent("""
        R0lGODlhDAAMAIQAAP//9/X
        17unp5WZmZgAAAOfn515eXv
        Pz7Y6OjuDg4J+fn5OTk6enp
        56enmleECcgggoBADs=mZmE
        """[1:-1]))

    expected = {'picture': picture}

    assert result == expected


sanity_args = [  # :off
    list_block,
    list_inline,
    dict_block,
    dict_inline,
    str_literal,
    str_folded,
    lists_of_dicts,
    dicts_of_lists,
    mark.xfail(node_anchors_and_references),
    casted_data_types,
    specified_data_types__binary
]  # :on


@mark.skipif
@mark.parametrize('sample', sanity_args)
def test__sanity(sample):
    load_result = pureyaml.load(sample)
    dump_result = pureyaml.dump(load_result)
    load_expected = pureyaml.load(dump_result)
    dump_expected = pureyaml.dump(load_expected)

    assert load_result == load_expected
    assert dump_result == dump_expected
