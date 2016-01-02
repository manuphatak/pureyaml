#!/usr/bin/env python
# coding=utf-8

"""
test_pureyaml
----------------------------------

Tests for `pureyaml` module.
"""
from textwrap import dedent

from pytest import mark

from pureyaml.nodes import *
from pureyaml.pureyaml import parser

skip = mark.skipif


def test_basic_single_doc():
    text = dedent("""
        ---
        Hello World
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')))

    assert nodes == expected


def test_doc_with_no_end_of_doc_indicator():
    text = dedent("""
        ---
        Hello World
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')))

    assert nodes == expected


def test_two_docs():
    text = dedent("""
        ---
        Hello World
        ...
        ---
        Foo Bar
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')), Doc(Str('Foo Bar')))

    assert nodes == expected


def test_three_docs():
    text = dedent("""
        ---
        Hello World
        ...
        ---
        Foo Bar
        ...
        ---
        More Docs
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    assert nodes == expected


def test_three_docs_no_end_of_doc_indicators():
    text = dedent("""
        ---
        Hello World
        ---
        Foo Bar
        ---
        More Docs
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    assert nodes == expected


def test_implicit_doc():
    text = dedent("""
        Hello World
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('Hello World'))

    assert nodes == expected


def test_scalar_int():
    text = dedent("""
        ---
        123
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Int(123)))
    assert nodes == expected


def test_one_item_sequence():
    text = dedent("""
        ---
        - Hello World
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(Str('Hello World', ))))

    assert nodes == expected


def test_two_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
    )))  # :on

    print(nodes)
    assert nodes == expected


def test_three_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        - More Sequence Items
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
        Str('More Sequence Items'),
    )))  # :on

    print(nodes)
    assert nodes == expected


def test_1_item_map():
    text = dedent("""
        ---
        Hello: World
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
    )))  # :on

    assert nodes == expected


def test_2_item_map():
    text = dedent("""
        ---
        Hello: World
        Foo: Bar
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
    )))  # :on

    assert nodes == expected


def test_3_item_map():
    text = dedent("""
        ---
        Hello: World
        Foo: Bar
        More: Map Items
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
        (Str('More'), Str('Map Items')),
    )))  # :on

    assert nodes == expected


def test_casting_implicit_int():
    text = dedent("""
        123
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Int(123))

    assert nodes == expected


def test_casting_quoted_string():
    text = dedent("""
        "123"
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('123'))

    assert nodes == expected


def test_casting_quoted_string_with_escaped_char():
    text = dedent(r"""
        "She said, \"I Like turtles\" and she meant it!"
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('She said, \\"I Like turtles\\" and she meant it!'))

    assert nodes == expected


def test_casting_implicit_float():
    text = dedent("""
        123.0
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Float(123.0))

    assert nodes == expected


def test_casting_implicit_float_no_leading_digit():
    text = dedent("""
        .123
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Float(.123))

    assert nodes == expected


def test_casting_explicit_float():
    text = dedent("""
        !!float 123
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Float(123))

    assert nodes == expected


def test_casting_explicit_str():
    text = dedent("""
        !!str 123
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str(123))

    assert nodes == expected


def test_casting_implicit_bool_true():
    text = dedent("""
        Yes
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Bool(True))

    assert nodes == expected


def test_casting_implicit_bool_false():
    text = dedent("""
        No
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Bool(False))

    assert nodes == expected


def test_casting_explicit_str_from_bool():
    text = dedent("""
        !!str Yes
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('Yes'))

    assert nodes == expected

def test_uses_context_for_disambigous_str():
    text = dedent("""
        Yes we have No bananas
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('Yes we have No bananas'))

    assert nodes == expected

