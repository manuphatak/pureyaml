#!/usr/bin/env python
# coding=utf-8

"""
test_pureyaml
----------------------------------

Tests for `pureyaml` module.
"""
from __future__ import absolute_import

from textwrap import dedent

from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import feature_not_supported

parser = YAMLParser(debug=True)


def parse(text):
    nodes = parser.parse(text)
    return nodes


def test_basic_single_doc():
    text = dedent("""
        ---
        Hello World
        ...
    """)[1:]
    expected = Docs(Doc(Str('Hello World')))

    assert parse(text) == expected


def test_doc_with_no_end_of_doc_indicator():
    text = dedent("""
        ---
        Hello World
    """)[1:]

    expected = Docs(Doc(Str('Hello World')))

    assert parse(text) == expected


def test_2_docs():
    text = dedent("""
        ---
        Hello World
        ...
        ---
        Foo Bar
        ...
    """)[1:]

    expected = Docs(Doc(Str('Hello World')), Doc(Str('Foo Bar')))

    assert parse(text) == expected


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

    expected = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    assert parse(text) == expected


def test_3_docs_no_end_of_doc_indicators():
    text = dedent("""
        ---
        Hello World
        ---
        Foo Bar
        ---
        More Docs
    """)[1:]

    expected = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    assert parse(text) == expected


def test_implicit_doc():
    text = dedent("""
        Hello World
    """)[1:]

    expected = Docs(Doc(Str('Hello World')))

    assert parse(text) == expected


def test_scalar_int():
    text = dedent("""
        ---
        123
        ...
    """)[1:]

    expected = Docs(Doc(Int(123)))
    assert parse(text) == expected


def test_1_item_sequence():
    text = dedent("""
        ---
        - Hello World
        ...
    """)[1:]

    expected = Docs(Doc(Sequence(Str('Hello World', ))))

    assert parse(text) == expected


def test_2_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        ...
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
    )))  # :on

    assert parse(text) == expected


def test_3_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        - More Sequence Items
        ...
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
        Str('More Sequence Items'),
    )))  # :on

    assert parse(text) == expected


def test_1_item_map():
    text = dedent("""
        ---
        Hello: World
        ...
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
    )))  # :on

    assert parse(text) == expected


def test_2_item_map():
    text = dedent("""
        ---
        Hello: World
        Foo: Bar
        ...
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
    )))  # :on

    assert parse(text) == expected


def test_3_item_map():
    text = dedent("""
        ---
        Hello: World
        Foo: Bar
        More: Map Items
        ...
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
        (Str('More'), Str('Map Items')),
    )))  # :on

    assert parse(text) == expected


def test_casting_implicit_int():
    text = dedent("""
        123
    """)[1:]

    expected = Docs(Doc(Int(123)))

    assert parse(text) == expected


def test_casting_doublequoted_string():
    text = dedent("""
        "123"
    """)[1:]

    expected = Docs(Doc(Str('123')))
    assert parse(text) == expected


def test_casting_doublequoted_string_with_escaped_char():
    text = dedent(r"""
        "She said, \"I Like turtles\" and she meant it!"
    """)[1:]

    expected = Docs(Doc(Str('She said, \\"I Like turtles\\" and she meant it!')))

    assert parse(text) == expected


def test_casting_singlequoted_string():
    text = dedent("""
        '123'
    """)[1:]

    expected = Docs(Doc(Str('123')))

    assert parse(text) == expected


def test_casting_singlequoted_string_with_escaped_char():
    text = dedent(r"""
        'She said, \'I Like turtles\' and she meant it!'
    """)[1:]

    expected = Docs(Doc(Str("She said, \\'I Like turtles\\' and she meant it!")))

    assert parse(text) == expected


def test_casting_implicit_float():
    text = dedent("""
        123.0
    """)[1:]

    expected = Docs(Doc(Float(123.0)))

    assert parse(text) == expected


def test_casting_implicit_float_no_leading_digit():
    text = dedent("""
        .123
    """)[1:]

    expected = Docs(Doc(Float(.123)))

    assert parse(text) == expected


def test_casting_explicit_float():
    text = dedent("""
        !!float 123
    """)[1:]

    expected = Docs(Doc(Float(123)))

    assert parse(text) == expected


def test_casting_explicit_str():
    text = dedent("""
        !!str 123
    """)[1:]

    expected = Docs(Doc(Str(123)))

    assert parse(text) == expected


def test_casting_implicit_bool_true():
    text = dedent("""
        Yes
    """)[1:]

    expected = Docs(Doc(Bool(True)))

    assert parse(text) == expected


def test_casting_implicit_bool_false():
    text = dedent("""
        No
    """)[1:]

    expected = Docs(Doc(Bool(False)))

    assert parse(text) == expected


def test_casting_explicit_str_from_bool():
    text = dedent("""
        !!str Yes
    """)[1:]

    expected = Docs(Doc(Str('Yes')))

    assert parse(text) == expected


def test_uses_context_for_disambiguated_str():
    text = dedent("""
        Yes we have No bananas
    """)[1:]

    expected = Docs(Doc(Str('Yes we have No bananas')))

    assert parse(text) == expected


def test_ignore_comment():
    text = dedent("""
        123 # an integer
    """)[1:]

    expected = Docs(Doc(Int(123)))

    assert parse(text) == expected


def test_map_with_scalars_and_comments():
    text = dedent("""
        ---
        a: 123                     # an integer
        b: "123"                   # a string, disambiguated by quotes
        c: 123.0                   # a float
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123))
    )))  # :on

    assert parse(text) == expected


def test_different_map_with_bool_and_comments():
    text = dedent("""
        ---
        f: !!str Yes               # a string via explicit type
        g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),
    )))  # :on

    assert parse(text) == expected


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

    assert parse(text) == expected


def test_unnecessary_indent_scalar_item():
    text = dedent("""
        ---
            123
        ...
    """)[1:]

    expected = Docs(Doc(Int('123')))

    assert parse(text) == expected


def test_unnecessary_indent_1_item():
    text = dedent("""
        ---
            - Casablanca
        ...
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on
    assert parse(text) == expected


def test_unnecessary_indent_1_item_with_comment():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
        ...
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on
    assert parse(text) == expected


def test_unnecessary_indent_2_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
    )))  # :on

    assert parse(text) == expected


def test_unnecessary_indent_3_items():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    assert parse(text) == expected


def test_unnecessary_indent_3_items_with_dedent():
    text = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
        ...
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    assert parse(text) == expected


@feature_not_supported
def test_empty_scalar():
    text = dedent("""
        ---
        Also a null: # Empty
    """)[1:]

    expected = Docs(Doc(Map((Str('Also a null'), Null(None)))))

    assert parse(text) == expected


def test_empty_scalar_double_quote():
    text = dedent("""
        ---
        Not a null: ""
    """)[1:]

    expected = Docs(Doc(Map((Str('Not a null'), Str('')))))

    assert parse(text) == expected


def test_scalar_types():
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

    assert parse(text) == expected


def test_unnecessary_indent_3_with_edge_items():
    # edges: numbers and text, bool 'No' and text, single quote
    text = dedent("""
        --- # Favorite movies
            - 21 Jump Street
            - se7en
            - North by Northwest
            - The Man Who Wasn't There
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('21 Jump Street'),
        Str('se7en'),
        Str('North by Northwest'),
        Str('The Man Who Wasn\'t There'),
    )))  # :on

    assert parse(text) == expected


def test_scalar_literal_1_line():
    text = dedent("""
        |
          literal
    """)[1:]

    expected = Docs(Doc(Str('literal\n')))

    assert parse(text) == expected


def test_scalar_literal_ascii_art():
    text = dedent("""
        --- |
          \//||\/||
          // ||  ||__
    """)[1:]

    expected = Docs(Doc(Str('\//||\/||\n// ||  ||__\n')))

    assert parse(text) == expected


def test_longer_scalar_literal_with_indents():
    text = dedent("""
        |
            There once was a short man from Ealing
            Who got on a bus to Darjeeling
               It said on the door
               "Please don't spit on the floor"
            So he carefully spat on the ceiling
    """)[1:]

    expected = Docs(Doc(Str(dedent("""
            There once was a short man from Ealing
            Who got on a bus to Darjeeling
               It said on the door
               "Please don't spit on the floor"
            So he carefully spat on the ceiling
        """)[1:])))

    assert parse(text) == expected


def test_map_with_literal_block():
    text = dedent("""
        data: |
          There once was a short man from Ealing
          Who got on a bus to Darjeeling
            It said on the door
            "Please don't spit on the floor"
          So he carefully spat on the ceiling
    """)[1:]

    expected = Docs(Doc(Map((Str('data'), Str(dedent("""
            There once was a short man from Ealing
            Who got on a bus to Darjeeling
              It said on the door
              "Please don't spit on the floor"
            So he carefully spat on the ceiling
        """)[1:])))))

    assert parse(text) == expected


def test_map_with_folded_block():
    text = dedent("""
        data: >
            Wrapped text
            will be folded
            into a single
            paragraph

            Blank lines denote
            paragraph breaks
    """)[1:]

    expected = Docs(Doc(Map((Str('data'), Str(dedent("""
            Wrapped text will be folded into a single paragraph
            Blank lines denote paragraph breaks
        """)[1:])))))

    assert parse(text) == expected


def test_sequence_of_map_1_item():
    text = dedent("""
        - first_name: John
          last_name: Smith
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Map(
            (Str('first_name'), Str('John')),
            (Str('last_name'), Str('Smith')),
        ),
    )))  # :on

    assert parse(text) == expected


def test_sequence_of_map_3_item():
    text = dedent("""
        - first_name: John
          last_name: Smith
        - first_name: Joe
          last_name: Sixpack
        - first_name: Jane
          last_name: Doe
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Map(
            (Str('first_name'), Str('John')),
            (Str('last_name'), Str('Smith')),
        ),
        Map(
            (Str('first_name'), Str('Joe')),
            (Str('last_name'), Str('Sixpack')),
        ),
        Map(
            (Str('first_name'), Str('Jane')),
            (Str('last_name'), Str('Doe')),
        ),
    )))  # :on

    assert parse(text) == expected


def test_sequence_of_sequences_1_item():
    text = dedent("""
        - - John Smith
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Sequence(
            Str('John Smith'),
        ),
    )))  # :on

    assert parse(text) == expected


def test_sequence_of_sequences_3_items():
    text = dedent("""
        - - John Smith
          - Joe Sixpack
          - Jane Doe
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Sequence(
            Str('John Smith'),
            Str('Joe Sixpack'),
            Str('Jane Doe'),
        ),
    )))  # :on

    assert parse(text) == expected


def test_sequence_of_mixed_items():
    text = dedent("""
        - - John Smith
          - Joe Sixpack
          - Jane Doe
        - Casablanca
        -
          hello: world
          foo: bar
          1 edge case: success
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Sequence(
            Str('John Smith'),
            Str('Joe Sixpack'),
            Str('Jane Doe'),
        ),
        Str('Casablanca'),
        Map(
            (Str('hello'), Str('world')),
            (Str('foo'), Str('bar')),
            (Str('1 edge case'), Str('success')),
        )
    )))  # :on

    assert parse(text) == expected


def test_map_of_sequences_1_item():
    text = dedent("""
        people:
          - John Smith
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('people'), Sequence(
            Str('John Smith'),
        )),
    )))  # :on

    assert parse(text) == expected


def test_map_of_sequences_many_items():
    text = dedent("""
        people:
          - John Smith
          - Joe Sixpack
          - Jane Doe
        places:
          - London
          - Australia
          - US

    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Str('people'),
            Sequence(
                Str('John Smith'),
                Str('Joe Sixpack'),
                Str('Jane Doe'),
            )
        ),
        (
            Str('places'),
            Sequence(
                Str('London'),
                Str('Australia'),
                Str('US'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_map_of_map_1_item():
    text = dedent("""
        customer:
            first_name:   Dorothy
            family_name:  Gale
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Str('customer'),
            Map(
                (Str('first_name'), Str('Dorothy')),
                (Str('family_name'), Str('Gale')),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_map_of_map_many_items():
    text = dedent("""
        customer:
            first_name:   Dorothy
            family_name:  Gale
        cashier:
            first_name:   Joe
            family_name:  Sixpack
        total: 20
        items:
            - doritos
            - soda
            - candy
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Str('customer'),
            Map(
                (Str('first_name'), Str('Dorothy')),
                (Str('family_name'), Str('Gale')),
            )
        ),
        (
            Str('cashier'),
            Map(
                (Str('first_name'), Str('Joe')),
                (Str('family_name'), Str('Sixpack')),
            )
        ),
        (
            Str('total'), Int(20)
        ),
        (
            Str('items'),
            Sequence(
                Str('doritos'),
                Str('soda'),
                Str('candy'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_1_item_flow_sequence():
    text = dedent("""
        --- # Shopping list
        [milk]
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('milk'),
    )))  # :on

    assert parse(text) == expected


def test_many_item_flow_sequence():
    text = dedent("""
        --- # Shopping list
        [milk, pumpkin pie, eggs, juice]
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Str('milk'),
        Str('pumpkin pie'),
        Str('eggs'),
        Str('juice'),
    )))  # :on

    assert parse(text) == expected


def test_1_item_flow_map():
    text = dedent("""
        --- # Inline Block
        {name: John Smith}
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('name'), Str('John Smith')),
    )))  # :on

    assert parse(text) == expected


def test_2_item_flow_map():
    text = dedent("""
        --- # Inline Block
        {name: John Smith, age: 33}
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('name'), Str('John Smith')),
        (Str('age'), Int(33)),
    )))  # :on

    assert parse(text) == expected


def test_mixed_sequence_of_maps():
    text = dedent("""
        - {name: John Smith, age: 33}
        - name: Mary Smith
          age: 27
    """)[1:]

    expected = Docs(Doc(Sequence(  # :off
        Map(
            (Str('name'), Str('John Smith')),
            (Str('age'), Int(33)),
        ),
        Map(
            (Str('name'), Str('Mary Smith')),
            (Str('age'), Int(27)),
        ),
    )))  # :on

    assert parse(text) == expected


def test_mixed_map_of_sequences():
    text = dedent("""
        men: [John Smith, Bill Jones]
        women:
          - Mary Smith
          - Susan Williams
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Str('men'),
            Sequence(
                Str('John Smith'),
                Str('Bill Jones'),
            )
        ),
        (
            Str('women'),
            Sequence(
                Str('Mary Smith'),
                Str('Susan Williams'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_map_of_sequences_with_no_indent():
    text = dedent("""
        men:
        - John Smith
        - Bill Jones
        women:
        - Mary Smith
        - Susan Williams
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Str('men'),
            Sequence(
                Str('John Smith'),
                Str('Bill Jones'),
            )
        ),
        (
            Str('women'),
            Sequence(
                Str('Mary Smith'),
                Str('Susan Williams'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


# noinspection SpellCheckingInspection
def test_cast_type_binary():
    text = dedent(u"""
        ---
        picture: !!binary |
            R0lGODlhDAAMAIQAAP//9/X
            17unp5WZmZgAAAOfn515eXv
            Pz7Y6OjuDg4J+fn5OTk6enp
            56enmleECcgggoBADs=mZmE
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Str('picture'),
            Binary(dedent("""
                R0lGODlhDAAMAIQAAP//9/X
                17unp5WZmZgAAAOfn515eXv
                Pz7Y6OjuDg4J+fn5OTk6enp
                56enmleECcgggoBADs=mZmE
            """)[1:-1])
        ),
    )))  # :on

    assert parse(text) == expected


def test_1_item_map_explicit_key():
    text = dedent("""
        ? Hello: World
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
    )))  # :on

    assert parse(text) == expected


def test_2_item_map_explicit_key():
    text = dedent("""
        ? Hello
        : World
        ? Foo
        : Bar
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
    )))  # :on

    assert parse(text) == expected


def test_3_item_map_explicit_key():
    text = dedent("""
        ? Hello
        : World
        ? Foo
        : Bar
        ? More
        : Map Items
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
        (Str('More'), Str('Map Items')),
    )))  # :on

    assert parse(text) == expected


def test_map_complex_key__key_sequence_expanded():
    text = dedent("""
        ?
          - Detroit Tigers
          - Chicago Cubs
        :
          - 2001-07-23
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Sequence(
                Str('Detroit Tigers'),
                Str('Chicago Cubs'),
            ),
            Sequence(
                Str('2001-07-23'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_map_complex_key__key_sequence_compact():
    text = dedent("""
        ? - Detroit Tigers
          - Chicago Cubs
        : - 2001-07-23
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Sequence(
                Str('Detroit Tigers'),
                Str('Chicago Cubs'),
            ),
            Sequence(
                Str('2001-07-23'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_map_complex_key__flow_sequence():
    text = dedent("""
        ? [ New York Yankees,
            Atlanta Braves ]
        : [ 2001-07-02, 2001-08-12,
            2001-08-14 ]
    """)[1:]

    expected = Docs(Doc(Map(  # :off
        (
            Sequence(
                Str('New York Yankees'),
                Str('Atlanta Braves'),
            ),
            Sequence(
                Str('2001-07-02'),
                Str('2001-08-12'),
                Str('2001-08-14'),
            )
        ),
    )))  # :on

    assert parse(text) == expected


def test_double_dedent():
    text = dedent("""
        people:
            John Smith:
                nickname: Ol' johnny boy
        places:
            US:
                capital: DC
    """)[1:]
    expected = Docs(Doc(  # :off
        Map(
            (
                Str('people'),
                Map(
                    (
                        Str('John Smith'),
                        Map(
                            (Str('nickname'), Str("Ol' johnny boy")),
                        ),
                    ),
                ),
            ),
            (
                Str('places'),
                Map(
                    (
                        Str('US'),
                        Map(
                            (Str('capital'), Str('DC')),
                        ),
                    ),
                ),
            ),
        ),
    ))  # :on
    assert parse(text) == expected


@feature_not_supported
def test_double_dedent__literal_end():
    text = dedent("""
        people:
            John Smith:
                short bio: <
                    I like turtles.
                    And green turtles.
                long bio: |
                    I like turtles.
                    And green turtles.
        places:
            US:
                capital: DC
    """)[1:]
    expected = Docs(Doc(  # :off
        Map(
            (
                Str('people'),
                Map(
                    (
                        Str('John Smith'),
                        Map(
                            (Str('short bio'), Str('I like turtles. And green turtles.')),
                            (Str('long bio'), Str('I like turtles.\nAnd green turtles.')),
                        ),
                    ),
                ),
            ),
            (
                Str('places'),
                Map(
                    (
                        Str('US'),
                        Map(
                            (Str('capital'), Str('DC')),
                        ),
                    ),
                ),
            ),
        ),
    ))  # :on
    assert parse(text) == expected
