#!/usr/bin/env python
# coding=utf-8

"""
test_pureyaml
----------------------------------

Tests for `pureyaml` module.
"""
from textwrap import dedent

from pytest import mark

from pureyaml.nodes import *  # noqa
from pureyaml.pureyaml import YAMLParser

skipif = mark.skipif
parser = YAMLParser(debug=True)


def test_basic_single_doc():
    text = dedent("""
        ---
        Hello World
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')))

    assert nodes == expected


def test_doc_with_no_end_of_doc_indicator():
    text = dedent("""
        ---
        Hello World
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')))

    assert nodes == expected


def test_2_docs():
    text = dedent("""
        ---
        Hello World
        ...
        ---
        Foo Bar
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')), Doc(Str('Foo Bar')))

    assert nodes == expected


def test_3_docs():
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
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    assert nodes == expected


def test_3_docs_no_end_of_doc_indicators():
    text = dedent("""
        ---
        Hello World
        ---
        Foo Bar
        ---
        More Docs
    """)[1:]

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
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Hello World')))

    assert nodes == expected


def test_scalar_int():
    text = dedent("""
        ---
        123
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Int(123)))
    assert nodes == expected


def test_1_item_sequence():
    text = dedent("""
        ---
        - Hello World
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(Str('Hello World', ))))

    assert nodes == expected


def test_2_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
    )))  # :on

    assert nodes == expected


def test_3_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        - More Sequence Items
        ...
    """)[1:]

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
    """)[1:]

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
    """)[1:]

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
    """)[1:]

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
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Int(123)))

    assert nodes == expected


def test_casting_doublequoted_string():
    text = dedent("""
        "123"
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('123')))
    assert nodes == expected


def test_casting_doublequoted_string_with_escaped_char():
    text = dedent(r"""
        "She said, \"I Like turtles\" and she meant it!"
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('She said, \\"I Like turtles\\" and she meant it!')))

    assert nodes == expected


def test_casting_singlequoted_string():
    text = dedent("""
        '123'
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('123')))

    assert nodes == expected


def test_casting_singlequoted_string_with_escaped_char():
    text = dedent(r"""
        'She said, \'I Like turtles\' and she meant it!'
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str("She said, \\'I Like turtles\\' and she meant it!")))

    assert nodes == expected


def test_casting_implicit_float():
    text = dedent("""
        123.0
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Float(123.0)))

    assert nodes == expected


def test_casting_implicit_float_no_leading_digit():
    text = dedent("""
        .123
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Float(.123)))

    assert nodes == expected


def test_casting_explicit_float():
    text = dedent("""
        !!float 123
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Float(123)))

    assert nodes == expected


def test_casting_explicit_str():
    text = dedent("""
        !!str 123
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str(123)))

    assert nodes == expected


def test_casting_implicit_bool_true():
    text = dedent("""
        Yes
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Bool(True)))

    assert nodes == expected


def test_casting_implicit_bool_false():
    text = dedent("""
        No
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Bool(False)))

    assert nodes == expected


def test_casting_explicit_str_from_bool():
    text = dedent("""
        !!str Yes
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Yes')))

    assert nodes == expected


def test_uses_context_for_disambiguated_str():
    text = dedent("""
        Yes we have No bananas
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('Yes we have No bananas')))

    assert nodes == expected


def test_ignore_comment():
    text = dedent("""
        123 # an integer
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Int(123)))

    assert nodes == expected


def test_map_with_scalars_and_comments():
    text = dedent("""
        ---
        a: 123                     # an integer
        b: "123"                   # a string, disambiguated by quotes
        c: 123.0                   # a float
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123))
    )))  # :on

    assert nodes == expected


def test_different_map_with_bools_and_comments():
    text = dedent("""
        ---
        f: !!str Yes               # a string via explicit type
        g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),
    )))  # :on

    assert nodes == expected


def test_longer_map_with_scalars_and_comments():
    text = dedent("""
        ---
        a: 123                     # an integer
        b: "123"                   # a string, disambiguated by quotes
        c: 123.0                   # a float
        d: !!float 123             # also a float via explicit data type prefixed by (!!)
        e: !!str 123               # a string, disambiguated by explicit type
        f: !!str Yes               # a string via explicit type
        g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
        h: Yes we have No bananas  # a string, "Yes" and "No" disambiguated by context.
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123)),
        (Str('d'), Float(123)),
        (Str('e'), Str(123)),
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),
        (Str('h'), Str('Yes we have No bananas')),

    )))  # :on

    assert nodes == expected


def test_unnecessary_indent_scalar_item():
    text = dedent("""
        ---
            123
        ...
    """)[1:]
    nodes = parser.parse(text)
    expected = Docs(Doc(Int('123')))

    assert nodes == expected


def test_unnecessary_indent_1_item():
    text = dedent("""
        ---
            - Casablanca
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on
    assert nodes == expected


def test_unnecessary_indent_1_item_with_comment():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on
    assert nodes == expected


def test_unnecessary_indent_2_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
    )))  # :on

    assert nodes == expected


def test_unnecessary_indent_3_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    assert nodes == expected


def test_unnecessary_indent_3_items_with_dedent():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
        ...
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    assert nodes == expected


def test_empty_scalar():
    text = dedent("""
        ---
        Also a null: # Empty
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map((Str('Also a null'), Null(None)))))

    assert nodes == expected


def test_empty_scalar_double_quote():
    text = dedent("""
        ---
        Not a null: ""
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map((Str('Not a null'), Str('')))))

    assert nodes == expected


def test_scalar_types():  # noqa
    # TODO uncomment lines
    text = dedent("""
        ---
        A null: null
        # Also a null: # Empty
        # Not a null: ""
        Booleans a: true
        Booleans b: True
        Booleans c: false
        Booleans d: FALSE
        Booleans e: Yes
        Booleans f: YES
        Booleans g: No
        Booleans h: no
        Integers a: 0
        Integers b: 0o7
        Integers c: 0x3A
        Integers d: -19
        Floats a: 0.
        Floats b: -0.0
        Floats c: .5
        Floats d: +12e03
        Floats e: -2E+05
        Also floats a: .inf
        Also floats b: -.Inf
        Also floats c: +.INF
        Also floats d: .NAN
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Map(  # :off
        (Str('A null'), Null('null')),
        # (Str('Also a null'), Null(None)),
        # (Str('Not a null'), Str('')),
        (Str('Booleans a'), Bool('true')),
        (Str('Booleans b'), Bool('True')),
        (Str('Booleans c'), Bool('false')),
        (Str('Booleans d'), Bool('False')),
        (Str('Booleans e'), Bool('Yes')),
        (Str('Booleans f'), Bool('YES')),
        (Str('Booleans g'), Bool('No')),
        (Str('Booleans h'), Bool('no')),
        (Str('Integers a'), Int(0)),
        (Str('Integers b'), Int(0o7)),
        (Str('Integers c'), Int(0x3A)),
        (Str('Integers d'), Int(-19)),
        (Str('Floats a'), Float(0.)),
        (Str('Floats b'), Float(-0.0)),
        (Str('Floats c'), Float(.5)),
        (Str('Floats d'), Float(+12e03)),
        (Str('Floats e'), Float(-2E+05)),
        (Str('Also floats a'), Float('.inf')),
        (Str('Also floats b'), Float('-.Inf')),
        (Str('Also floats c'), Float('+.INF')),
        (Str('Also floats d'), Float('.nan')),
    )))  # :on

    def diff():
        actual_map, expected_map = nodes.value[0].value[0].value, expected.value[0].value[0].value
        for (a_k, a_v), (e_k, e_v) in zip(actual_map, expected_map):

            if a_k.value != e_k.value:
                left_length, right_length = len(str(a_k)), len(str(e_k))
                print('Keys mismatched')
                print('    | %s != %s' % (a_k, e_k))
                print('    | %s  != %s' % (  # :off
                    str(a_k.value).rjust(left_length - 1),
                    str(e_k.value).rjust(right_length-1)
                ))  # :on
            if a_v.value != e_v.value:
                left_length, right_length = len(str(a_v)), len(str(e_v))
                print('Values mismatched')
                print('    | %s != %s' % (a_v, e_v))
                print('    | %s  != %s' % (  # :off
                    str(a_v.value).rjust(left_length - 1),
                    str(e_v.value).rjust(right_length-1)
                ))  # :on
            if a_k.value != e_k.value:
                break

    assert nodes == expected, diff()


def test_unnecessary_indent_3_with_edge_items():
    # edges: numbers and text, bool 'No' and text, single quote
    text = dedent("""
        --- # Favorite movies
            - 21 Jump Street
            - se7en
            - North by Northwest
            - The Man Who Wasn't There
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        Str('21 Jump Street'),
        Str('se7en'),
        Str('North by Northwest'),
        Str('The Man Who Wasn\'t There'),
    )))  # :on

    assert nodes == expected


def test_scalar_literal_1_line():
    text = dedent("""
        |
          literal
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('literal')))

    assert nodes == expected


def test_scalar_literal_ascii_art():
    text = dedent("""
        --- |
          \//||\/||
          // ||  ||__
    """)[1:]

    nodes = parser.parse(text)
    expected = Docs(Doc(Str('\//||\/||\n// ||  ||__')))

    assert nodes == expected
