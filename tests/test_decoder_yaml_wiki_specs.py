#!/usr/bin/env python
# coding=utf-8
"""
source: https://en.wikipedia.org/wiki/YAML#Basic_components_of_YAML
"""
from __future__ import absolute_import

from textwrap import dedent

from pytest import mark

import pureyaml
from tests.utils import feature_not_supported


def load(text):
    obj = pureyaml.load(text)
    return obj


def test_can_read_list_block():
    text = dedent("""
    --- # Favorite movies
        - Casablanca
        - North by Northwest
        - The Man Who Wasn't There
    """)[1:]

    assert load(text) == ['Casablanca', 'North by Northwest', 'The Man Who Wasn\'t There']


def test_can_read_list_inline():
    text = dedent("""
    --- # Shopping list
    [milk, pumpkin pie, eggs, juice]
    """)[1:]

    assert load(text) == ['milk', 'pumpkin pie', 'eggs', 'juice']


def test_can_read_dict_block():
    text = dedent("""
    --- # Indented Block
        name: John Smith
        age: 33
    """)[1:]

    expected = {'name': 'John Smith', 'age': 33}

    assert load(text) == expected


def test_can_read_dict_inline():
    text = dedent("""
    {name: John Smith, age: 33}
    """)[1:]

    expected = {'name': 'John Smith', 'age': 33}

    assert load(text) == expected


def test_can_read_str_literal():
    text = dedent("""
    data: |
        There once was a short man from Ealing
        Who got on a bus to Darjeeling
            It said on the door
            "Please don't spit on the floor"
        So he carefully spat on the ceiling
    """)[1:]

    data = dedent("""
        There once was a short man from Ealing
        Who got on a bus to Darjeeling
            It said on the door
            "Please don't spit on the floor"
        So he carefully spat on the ceiling
        """[1:-1])

    expected = {'data': data}

    assert load(text) == expected


def test_can_read_str_folded():
    text = dedent("""
    data: >
        Wrapped text
        will be folded
        into a single
        paragraph

        Blank lines denote
        paragraph breaks
    """)[1:]
    data = "Wrapped text will be folded into a single paragraph\nBlank lines denote paragraph breaks\n"

    expected = {'data': data}
    assert load(text) == expected


def test_can_read_lists_of_dicts():
    text = dedent("""
    - {name: John Smith, age: 33}
    - name: Mary Smith
      age: 27
    """)[1:]
    expected = [  # :off
        {'name': 'John Smith', 'age': 33},
        {'name': 'Mary Smith', 'age': 27}
    ]  # :on

    assert load(text) == expected


def test_can_read_dicts_of_lists():
    text = dedent("""
        men: [John Smith, Bill Jones]
        women:
            - Mary Smith
            - Susan Williams
    """)[1:]
    expected = {  # :off
        'men': ['John Smith', 'Bill Jones'],
        'women': ['Mary Smith', 'Susan Williams']
    }  # :on

    assert load(text) == expected


@feature_not_supported
def test_can_read_node_anchors_and_references():
    text = dedent("""
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

    assert load(text) == expected


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
    data = load(casted_data_types)
    assert isinstance(data[key], type_)


def test_can_read_values_from_casted_data__str_from_int():
    data = load(casted_data_types)
    assert data['e'] == '123'


def test_can_read_values_from_casted_data__str_from_keyword():
    data = load(casted_data_types)
    assert data['f'] == 'Yes'


def test_can_read_values_from_casted_data__bool():
    data = load(casted_data_types)
    assert data['g'] is True


def test_can_read_values_from_casted_data__str_from_context():
    data = load(casted_data_types)
    assert data['h'] == 'Yes we have No bananas'


def test_can_cast_binary():
    # noinspection SpellCheckingInspection
    text = dedent("""
    ---
    picture: !!binary |
        R0lGODlhDAAMAIQAAP//9/X
        17unp5WZmZgAAAOfn515eXv
        Pz7Y6OjuDg4J+fn5OTk6enp
        56enmleECcgggoBADs=mZmE
    """)[1:]
    # noinspection SpellCheckingInspection
    picture = (b"GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee"
               b"\xe9\xe9\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e"
               b"\x8e\x8e\xe0\xe0\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7"
               b"\x9e\x9e\x9ei^\x10' \x82\n\x01\x00;")

    expected = {'picture': picture}

    assert load(text) == expected


def test_travis_yml():
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
    text = dedent("""
        # This file was autogenerated and will overwrite each time you run travis_pypi_setup.py
        env:
        - TOXENV=py26
        - TOXENV=py27
        - TOXENV=py33
        - TOXENV=py34
        - TOXENV=py35
        - TOXENV=pypy
        - TOXENV=docs
        install:
        - pip install tox coveralls
        language: python
        python:
        - '3.5'
        script:
        - tox -e $TOXENV
        after_success:
        - coveralls
        deploy:
          true:
            condition: $TOXENV == py34
            repo: bionikspoon/pureyaml
            tags: true
          distributions: sdist bdist_wheel
          password:
            secure: {secure_block}
          provider: pypi
          user: bionikspoon

    """)[1:].format(secure_block=secure_block)

    expected = {  # :off
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

    actual = load(text)
    assert actual == expected

#
# sanity_args = [  # :off
#     list_block,
#     list_inline,
#     dict_block,
#     dict_inline,
#     feature_not_supported(str_literal),
#     feature_not_supported(str_folded),
#     lists_of_dicts,
#     dicts_of_lists,
#     feature_not_supported(node_anchors_and_references),
#     feature_not_supported(casted_data_types),
#     feature_not_supported(specified_data_types__binary),
# ]  # :on
#
# sanity_names = [  # :off
#     'list_block',
#     'list_inline',
#     'dict_block',
#     'dict_inline',
#     'str_literal',
#     'str_folded',
#     'lists_of_dicts',
#     'dicts_of_lists',
#     'node_anchors_and_references',
#     'casted_data_types',
#     'specified_data_types__binary',
# ]  # :on
#
#
# # @feature_not_supported
# @mark.parametrize('sample', sanity_args, False, sanity_names)
# def test__sanity(sample):
#     load_result = pureyaml.load(sample)
#     dump_result = pureyaml.dump(load_result)
#     load_expected = pureyaml.load(dump_result)
#     dump_expected = pureyaml.dump(load_expected)
#
#     assert load_result == load_expected
#     assert dump_result == dump_expected
