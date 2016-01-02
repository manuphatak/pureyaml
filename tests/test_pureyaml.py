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


def test_casting_doublequoted_string():
    text = dedent("""
        "123"
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('123'))

    assert nodes == expected


def test_casting_doublequoted_string_with_escaped_char():
    text = dedent(r"""
        "She said, \"I Like turtles\" and she meant it!"
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('She said, \\"I Like turtles\\" and she meant it!'))

    assert nodes == expected


def test_casting_singlequoted_string():
    text = dedent("""
        '123'
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('123'))

    assert nodes == expected


def test_casting_singlequoted_string_with_escaped_char():
    text = dedent(r"""
        'She said, \'I Like turtles\' and she meant it!'
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str("She said, \\'I Like turtles\\' and she meant it!"))

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


@skip
def test_uses_context_for_disambiguated_str():
    # TODO make this work
    text = dedent("""
        Yes we have No bananas
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('Yes we have No bananas'))

    assert nodes == expected


def test_ignore_comment():
    text = dedent("""
        123 # an integer
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Int(123))

    assert nodes == expected


def test_map_with_scalars_and_comments():
    text = dedent("""
        ---
        a: 123                     # an integer
        b: "123"                   # a string, disambiguated by quotes
        c: 123.0                   # a float
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123))
    ))  # :on

    assert nodes == expected


def test_different_map_with_bools_and_comments():
    text = dedent("""
        ---
        f: !!str Yes               # a string via explicit type
        g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Map(  # :off
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),
    ))  # :on

    assert nodes == expected


def test_longer_map_with_scalars_and_comments():
    # TODO uncomment H
    text = dedent("""
        ---
        a: 123                     # an integer
        b: "123"                   # a string, disambiguated by quotes
        c: 123.0                   # a float
        d: !!float 123             # also a float via explicit data type prefixed by (!!)
        e: !!str 123               # a string, disambiguated by explicit type
        f: !!str Yes               # a string via explicit type
        g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
        # h: Yes we have No bananas  # a string, "Yes" and "No" disambiguated by context.
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123)),
        (Str('d'), Float(123)),
        (Str('e'), Str(123)),
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),

    ))  # :on

    assert nodes == expected


@skip
def test_unnecessary_indent_1_item():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on

    assert nodes == expected


@skip
def test_unnecessary_indent_2_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
    )))  # :on

    assert nodes == expected


@skip
def test_unnecessary_indent_3_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    assert nodes == expected


@skip
def test_unnecessary_indent_1_item_no_dedent():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on

    assert nodes == expected


@skip
def test_unnecessary_indent_3_with_edge_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - North by Northwest
            - The Man Who Wasn't There
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('North by Northwest'),
        Str('The Man Who Wasn\'t There'),
    )))  # :on

    assert nodes == expected


@skip
def test_scalar_literal_one_line():
    text = dedent("""
        |
          literal
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Doc(Str('literal'))

    assert nodes == expected


@skip
def test_scalar_literal_ascii_art():
    text = dedent("""
        --- |
          \//||\/||
          // ||  ||__
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')))

    assert nodes == expected
