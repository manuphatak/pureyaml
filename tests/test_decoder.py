#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

import yaml as pyyaml
from pytest import mark

import pureyaml
from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import MultiTestCaseBase


class DecoderTestCase(MultiTestCaseBase):
    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_basic_single_doc__data = dedent("""
        ---
        Hello World
        ...
    """)[1:]
    it_handles_basic_single_doc__test_parser = Docs(Doc(Str('Hello World')))
    it_handles_basic_single_doc__test_sanity = None
    it_handles_basic_single_doc__test_pureyaml_pyyaml = 'Hello World'

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_doc_with_no_end_of_doc_indicator__data = dedent("""
        ---
        Hello World
    """)[1:]
    it_handles_doc_with_no_end_of_doc_indicator__test_parser = Docs(Doc(  # :off
        Str('Hello World')
    ))  # :on
    it_handles_doc_with_no_end_of_doc_indicator__test_sanity = None
    it_handles_doc_with_no_end_of_doc_indicator__test_pureyaml_pyyaml = 'Hello World'

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_2_docs__data = dedent("""
        ---
        Hello World
        ...
        ---
        Foo Bar
        ...
    """)[1:]

    it_handles_2_docs__test_pureyaml_pyyaml__skip = None
    it_handles_2_docs__test_sanity = None
    it_handles_2_docs__test_parser = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar'))
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_3_docs__data = dedent("""
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

    it_handles_3_docs__test_pureyaml_pyyaml__skip = None
    it_handles_3_docs__test_sanity = None
    it_handles_3_docs__test_parser = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_3_docs_no_end_of_doc_indicators__data = dedent("""
        ---
        Hello World
        ---
        Foo Bar
        ---
        More Docs
    """)[1:]

    it_handles_3_docs_no_end_of_doc_indicators__test_pureyaml_pyyaml__skip = None
    it_handles_3_docs_no_end_of_doc_indicators__test_sanity = None
    it_handles_3_docs_no_end_of_doc_indicators__test_parser = Docs(  # :off
        Doc(Str('Hello World')),
        Doc(Str('Foo Bar')),
        Doc(Str('More Docs'))
    )  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_implicit_doc__data = dedent("""
        Hello World
    """)[1:]

    it_handles_implicit_doc__test_sanity = None

    it_handles_implicit_doc__test_pureyaml_pyyaml = 'Hello World'
    it_handles_implicit_doc__test_parser = Docs(Doc(Str('Hello World')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_scalar_int__data = dedent("""
        ---
        123
        ...
    """)[1:]

    it_handles_scalar_int__test_sanity = None

    it_handles_scalar_int__test_pureyaml_pyyaml = 123
    it_handles_scalar_int__test_parser = Docs(Doc(Int(123)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_1_item_sequence__data = dedent("""
        ---
        - Hello World
        ...
    """)[1:]

    it_handles_1_item_sequence__test_sanity = None

    it_handles_1_item_sequence__test_pureyaml_pyyaml = ['Hello World']
    it_handles_1_item_sequence__test_parser = Docs(Doc(Sequence(  # :off
        Str('Hello World')
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_2_item_sequence__data = dedent("""
        ---
        - Hello World
        - Foo Bar
        ...
    """)[1:]

    it_handles_2_item_sequence__test_sanity = None

    it_handles_2_item_sequence__test_pureyaml_pyyaml = ['Hello World', 'Foo Bar']
    it_handles_2_item_sequence__test_parser = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_3_item_sequence__data = dedent("""
        ---
        - Hello World
        - Foo Bar
        - More Sequence Items
        ...
    """)[1:]

    it_handles_3_item_sequence__test_sanity = None

    it_handles_3_item_sequence__test_pureyaml_pyyaml = [  # :off
        'Hello World',
        'Foo Bar',
        'More Sequence Items'
    ]  # :on
    it_handles_3_item_sequence__test_parser = Docs(Doc(Sequence(  # :off
        Str('Hello World'),
        Str('Foo Bar'),
        Str('More Sequence Items'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_1_item_map__data = dedent("""
        ---
        Hello: World
        ...
    """)[1:]

    it_handles_1_item_map__test_sanity = None

    it_handles_1_item_map__test_pureyaml_pyyaml = {'Hello': 'World'}
    it_handles_1_item_map__test_parser = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_2_item_map__data = dedent("""
        ---
        Hello: World
        Foo: Bar
        ...
    """)[1:]

    it_handles_2_item_map__test_sanity = None

    it_handles_2_item_map__test_pureyaml_pyyaml = {  # :off
        'Foo': 'Bar',
        'Hello': 'World'
    }  # :on
    it_handles_2_item_map__test_parser = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_3_item_map__data = dedent("""
        ---
        Hello: World
        Foo: Bar
        More: Map Items
        ...
    """)[1:]

    it_handles_3_item_map__test_sanity = None

    it_handles_3_item_map__test_pureyaml_pyyaml = {  # :off
        'Foo': 'Bar',
        'Hello': 'World',
        'More': 'Map Items'
    }  # :on
    it_handles_3_item_map__test_parser = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
        (Str('More'), Str('Map Items')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_implicit_int__data = dedent("""
        123
    """)[1:]

    it_handles_casting_implicit_int__test_sanity = None
    it_handles_casting_implicit_int__test_pureyaml_pyyaml = 123
    it_handles_casting_implicit_int__test_parser = Docs(Doc(Int(123)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_doublequoted_string__data = dedent("""
        "123"
    """)[1:]

    it_handles_casting_doublequoted_string__test_sanity = None
    it_handles_casting_doublequoted_string__test_pureyaml_pyyaml = '123'
    it_handles_casting_doublequoted_string__test_parser = Docs(Doc(Str('123')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_doublequoted_string_with_escaped_char__data = dedent(r"""
        "She said, \"I Like turtles\" and she meant it!"
    """)[1:]

    it_handles_casting_doublequoted_string_with_escaped_char__test_sanity = None
    it_handles_casting_doublequoted_string_with_escaped_char__test_pureyaml_pyyaml = (  # :off
        'She said, "I Like turtles" and she meant it!'
    )  # :on
    it_handles_casting_doublequoted_string_with_escaped_char__test_parser = Docs(
        Doc(Str('She said, "I Like turtles" and she meant it!')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_singlequoted_string__data = dedent("""
        '123'
    """)[1:]

    it_handles_casting_singlequoted_string__test_sanity = None
    it_handles_casting_singlequoted_string__test_pureyaml_pyyaml = '123'
    it_handles_casting_singlequoted_string__test_parser = Docs(Doc(Str('123')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_singlequoted_string_with_escaped_char__data = dedent(r"""
        She said, 'I Like turtles' and she meant it!
    """)[1:]

    it_handles_casting_singlequoted_string_with_escaped_char__test_sanity = None
    it_handles_casting_singlequoted_string_with_escaped_char__test_pureyaml_pyyaml = dedent(r"""
        She said, 'I Like turtles' and she meant it!
    """)[1:-1]
    it_handles_casting_singlequoted_string_with_escaped_char__test_parser = Docs(
        Doc(Str("She said, 'I Like turtles' and she meant it!")))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_implicit_float__data = dedent("""
        123.0
    """)[1:]

    it_handles_casting_implicit_float__test_sanity = None
    it_handles_casting_implicit_float__test_pureyaml_pyyaml = 123.0
    it_handles_casting_implicit_float__test_parser = Docs(Doc(Float(123.0)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_implicit_float_no_leading_digit__data = dedent("""
        .123
    """)[1:]

    it_handles_casting_implicit_float_no_leading_digit__test_sanity = None
    it_handles_casting_implicit_float_no_leading_digit__test_pureyaml_pyyaml = 0.123
    it_handles_casting_implicit_float_no_leading_digit__test_parser = Docs(Doc(Float(.123)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_explicit_float__data = dedent("""
        !!float 123
    """)[1:]

    it_handles_casting_explicit_float__test_sanity = None
    it_handles_casting_explicit_float__test_pureyaml_pyyaml = 123.0
    it_handles_casting_explicit_float__test_parser = Docs(Doc(Float(123)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_explicit_str__data = dedent("""
        !!str 123
    """)[1:]

    it_handles_casting_explicit_str__test_sanity = None
    it_handles_casting_explicit_str__test_pureyaml_pyyaml = '123'
    it_handles_casting_explicit_str__test_parser = Docs(Doc(Str(123)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_implicit_bool_true__data = dedent("""
        Yes
    """)[1:]

    it_handles_casting_implicit_bool_true__test_sanity = None
    it_handles_casting_implicit_bool_true__test_pureyaml_pyyaml = True
    it_handles_casting_implicit_bool_true__test_parser = Docs(Doc(Bool(True)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_implicit_bool_false__data = dedent("""
        No
    """)[1:]

    it_handles_casting_implicit_bool_false__test_sanity = None
    it_handles_casting_implicit_bool_false__test_pureyaml_pyyaml = False
    it_handles_casting_implicit_bool_false__test_parser = Docs(Doc(Bool(False)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_casting_explicit_str_from_bool__data = dedent("""
        !!str Yes
    """)[1:]

    it_handles_casting_explicit_str_from_bool__test_sanity = None
    it_handles_casting_explicit_str_from_bool__test_pureyaml_pyyaml = 'Yes'
    it_handles_casting_explicit_str_from_bool__test_parser = Docs(Doc(Str('Yes')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_uses_context_for_disambiguated_str__data = dedent("""
        Yes we have No bananas
    """)[1:]

    it_uses_context_for_disambiguated_str__test_sanity = None
    it_uses_context_for_disambiguated_str__test_pureyaml_pyyaml = 'Yes we have No bananas'
    it_uses_context_for_disambiguated_str__test_parser = Docs(Doc(Str('Yes we have No bananas')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_ignore_comment__data = dedent("""
        123 # an integer
    """)[1:]

    it_handles_ignore_comment__test_sanity = None

    it_handles_ignore_comment__test_pureyaml_pyyaml = 123
    it_handles_ignore_comment__test_parser = Docs(Doc(Int(123)))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_with_scalars_and_comments__data = dedent("""
        ---
        a: 123                     # an integer
        b: "123"                   # a string, disambiguated by quotes
        c: 123.0                   # a float
    """)[1:]

    it_handles_map_with_scalars_and_comments__test_sanity = None
    it_handles_map_with_scalars_and_comments__test_pureyaml_pyyaml = {  # :off
        'a': 123,
        'b': '123',
        'c': 123.0
    }  # :on
    it_handles_map_with_scalars_and_comments__test_parser = Docs(Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123))
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_different_map_with_bool_and_comments__data = dedent("""
        ---
        f: !!str Yes               # a string via explicit type
        g: Yes                     # a boolean True (yaml1.1), string "Yes" (yaml1.2)
    """)[1:]

    it_handles_different_map_with_bool_and_comments__test_sanity = None
    it_handles_different_map_with_bool_and_comments__test_pureyaml_pyyaml = {'g': True, 'f': 'Yes'}
    it_handles_different_map_with_bool_and_comments__test_parser = Docs(Doc(Map(  # :off
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_longer_map_with_scalars_and_comments__data = dedent("""
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

    it_handles_longer_map_with_scalars_and_comments__test_sanity = None
    it_handles_longer_map_with_scalars_and_comments__test_pureyaml_pyyaml = {  # :off
        'b': '123',
        'h': 'Yes we have No bananas',
        'a': 123,
        'd': 123.0,
        'g': True,
        'c': 123.0,
        'f': 'Yes',
        'e': '123'
    }  # :on
    it_handles_longer_map_with_scalars_and_comments__test_parser = Docs(Doc(Map(  # :off
        (Str('a'), Int(123)),
        (Str('b'), Str(123)),
        (Str('c'), Float(123)),
        (Str('d'), Float(123)),
        (Str('e'), Str(123)),
        (Str('f'), Str('Yes')),
        (Str('g'), Bool('Yes')),
        (Str('h'), Str('Yes we have No bananas')),

    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_unnecessary_indent_scalar_item__data = dedent("""
        ---
            123
        ...
    """)[1:]

    it_handles_unnecessary_indent_scalar_item__test_sanity = None
    it_handles_unnecessary_indent_scalar_item__test_pureyaml_pyyaml = 123
    it_handles_unnecessary_indent_scalar_item__test_parser = Docs(Doc(Int('123')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_unnecessary_indent_1_item__data = dedent("""
        ---
            - Casablanca
        ...
    """)[1:]

    it_handles_unnecessary_indent_1_item__test_sanity = None
    it_handles_unnecessary_indent_1_item__test_pureyaml_pyyaml = ['Casablanca']
    it_handles_unnecessary_indent_1_item__test_parser = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_unnecessary_indent_1_item_with_comment__data = dedent("""
        --- # Favorite movies
            - Casablanca
        ...
    """)[1:]

    it_handles_unnecessary_indent_1_item_with_comment__test_sanity = None
    it_handles_unnecessary_indent_1_item_with_comment__test_pureyaml_pyyaml = ['Casablanca']
    it_handles_unnecessary_indent_1_item_with_comment__test_parser = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_unnecessary_indent_2_items__data = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
    """)[1:]

    it_handles_unnecessary_indent_2_items__test_sanity = None
    it_handles_unnecessary_indent_2_items__test_pureyaml_pyyaml = [  # :off
        'Casablanca',
        'South by Southwest'
    ]  # :on
    it_handles_unnecessary_indent_2_items__test_parser = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_unnecessary_indent_3_items__data = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
    """)[1:]

    it_handles_unnecessary_indent_3_items__test_sanity = None
    it_handles_unnecessary_indent_3_items__test_pureyaml_pyyaml = [  # :off
        'Casablanca',
        'South by Southwest',
        'The Man Who Wasnt There'
    ]  # :on
    it_handles_unnecessary_indent_3_items__test_parser = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_unnecessary_indent_3_items_with_dedent__data = dedent("""
        --- # Favorite movies
            - Casablanca
            - South by Southwest
            - The Man Who Wasnt There
        ...
    """)[1:]

    it_handles_unnecessary_indent_3_items_with_dedent__test_sanity = None
    it_handles_unnecessary_indent_3_items_with_dedent__test_pureyaml_pyyaml = [  # :off
        'Casablanca',
        'South by Southwest',
        'The Man Who Wasnt There'
    ]  # :on
    it_handles_unnecessary_indent_3_items_with_dedent__test_parser = Docs(Doc(Sequence(  # :off
        Str('Casablanca'),
        Str('South by Southwest'),
        Str('The Man Who Wasnt There'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_empty_scalar__data = dedent("""
        ---
        Also a null: # Empty
    """)[1:]

    it_handles_empty_scalar__test_pureyaml_sanity__xfail = None
    it_handles_empty_scalar__test_pyyaml = {'Also a null': None}
    it_handles_empty_scalar__test_parser__xfail = Docs(Doc(Map(  # :off
        (Str('Also a null'), Null(None))
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_empty_scalar_double_quote__data = dedent("""
        ---
        Not a null: ""
    """)[1:]

    it_handles_empty_scalar_double_quote__test_pureyaml_pyyaml = {'Not a null': ''}
    it_handles_empty_scalar_double_quote__test_sanity = None
    it_handles_empty_scalar_double_quote__test_parser = Docs(Doc(Map(  # :off
        (Str('Not a null'), Str(''))
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    # PyYaml Floats/Int not supported.
    #  TODO uncomment lines
    it_handles_scalar_types__data = dedent("""
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
        # Also floats d: .NAN
    """)[1:]

    it_handles_scalar_types__test_pureyaml_sanity = {  # :off
        'Integers b': 0o7,
        'A null': None,
        'Booleans c': False,
        'Booleans e': True,
        'Integers d': -19,
        'Booleans a': True,
        'Also floats c': float('inf'),
        'Floats a': 0.0,
        'Booleans b': True,
        'Floats d': float('+12e03'),
        'Booleans h': False,
        'Booleans g': False,
        'Floats c': 0.5,
        'Floats b': -0.0,
        'Booleans d': False,
        'Also floats b': float('-inf'),
        'Booleans f': True,
        'Floats e': float('-2E+05'),
        'Also floats a': float('inf'),
        'Integers a': 0,
        # 'Also floats d': float('nan'),
        'Integers c': 58
    }  # :on

    it_handles_scalar_types__test_pyyaml__skip = None
    it_handles_scalar_types__test_parser = Docs(Doc(Map(  # :off
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
        # (Str('Also floats d'), Float('.nan')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    #  edges: numbers and text,
    # bool 'No' and text, single quote
    it_handles_unnecessary_indent_3_with_edge_items__data = dedent("""
        --- # Favorite movies
            - 21 Jump Street
            - se7en
            - North by Northwest
            - The Man Who Wasn't There
    """)[1:]

    it_handles_unnecessary_indent_3_with_edge_items__test_sanity = None
    it_handles_unnecessary_indent_3_with_edge_items__test_pureyaml_pyyaml = [  # :off
        '21 Jump Street',
        'se7en',
        'North by Northwest',
        "The Man Who Wasn't There"
    ]  # :on
    it_handles_unnecessary_indent_3_with_edge_items__test_parser = Docs(Doc(Sequence(  # :off
        Str('21 Jump Street'),
        Str('se7en'),
        Str('North by Northwest'),
        Str('The Man Who Wasn\'t There'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_scalar_literal_1_line__data = dedent("""
        |
          literal
    """)[1:]

    it_handles_scalar_literal_1_line__test_pureyaml_pyyaml = 'literal\n'
    it_handles_scalar_literal_1_line__test_sanity = None
    it_handles_scalar_literal_1_line__test_parser = Docs(Doc(Str('literal\n')))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_scalar_literal_ascii_art__data = dedent("""
        --- |
          \//||\/||
          // ||  ||__
    """)[1:]

    it_handles_scalar_literal_ascii_art__test_pureyaml_pyyaml = (  # :off
        '\\//||\\/||\n// ||  ||__\n'
    )  # :on
    it_handles_scalar_literal_ascii_art__test_sanity = None
    it_handles_scalar_literal_ascii_art__test_parser = Docs(Doc(  # :off
        Str('\//||\/||\n// ||  ||__\n')
    ))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_longer_scalar_literal_with_indents__data = dedent("""
        |
            There once was a short man from Ealing
            Who got on a bus to Darjeeling
               It said on the door
               "Please don't spit on the floor"
            So he carefully spat on the ceiling
    """)[1:]

    it_handles_longer_scalar_literal_with_indents__test_pureyaml_pyyaml = (  # :off
        'There once was a short man from Ealing\n'
        'Who got on a bus to Darjeeling\n'
        '   It said on the door\n'
        '   "Please don\'t spit on the floor"\n'
        'So he carefully spat on the ceiling\n'
    )  # :on
    it_handles_longer_scalar_literal_with_indents__test_sanity = None
    it_handles_longer_scalar_literal_with_indents__test_parser = Docs(Doc(Str(dedent("""
            There once was a short man from Ealing
            Who got on a bus to Darjeeling
               It said on the door
               "Please don't spit on the floor"
            So he carefully spat on the ceiling
        """)[1:])))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_with_literal_block__data = dedent("""
        data: |
          There once was a short man from Ealing
          Who got on a bus to Darjeeling
            It said on the door
            "Please don't spit on the floor"
          So he carefully spat on the ceiling
    """)[1:]

    it_handles_map_with_literal_block__test_pureyaml_pyyaml = {  # :off
        'data': (
            'There once was a short man from Ealing\n'
            'Who got on a bus to Darjeeling\n'
            '  It said on the door\n'
            '  "Please don\'t spit on the floor"\n'
            'So he carefully spat on the ceiling\n'
        )
    }  # :on
    it_handles_map_with_literal_block__test_sanity = None
    it_handles_map_with_literal_block__test_parser = Docs(Doc(Map(  # :off
        (
            Str('data'),
            Str(dedent("""
                There once was a short man from Ealing
                Who got on a bus to Darjeeling
                  It said on the door
                  "Please don't spit on the floor"
                So he carefully spat on the ceiling
            """)[1:])
        )
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_with_folded_block__data = dedent("""
        data: >
            Wrapped text
            will be folded
            into a single
            paragraph

            Blank lines denote
            paragraph breaks
    """)[1:]

    it_handles_map_with_folded_block__test_pureyaml_pyyaml = {  # :off
        'data': (
            'Wrapped text will be folded into a single paragraph\n'
            'Blank lines denote paragraph breaks\n'
        )
    }  # :on
    it_handles_map_with_folded_block__test_sanity = None
    it_handles_map_with_folded_block__test_parser = Docs(Doc(Map((Str('data'), Str(dedent("""
            Wrapped text will be folded into a single paragraph
            Blank lines denote paragraph breaks
        """)[1:])))))

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_sequence_of_map_1_item__data = dedent("""
        - first_name: John
          last_name: Smith
    """)[1:]

    it_handles_sequence_of_map_1_item__test_sanity = None
    it_handles_sequence_of_map_1_item__test_pureyaml_pyyaml = [{'first_name': 'John', 'last_name': 'Smith'}]
    it_handles_sequence_of_map_1_item__test_parser = Docs(Doc(Sequence(  # :off
        Map(
            (Str('first_name'), Str('John')),
            (Str('last_name'), Str('Smith')),
        ),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_sequence_of_map_3_item__data = dedent("""
        - first_name: John
          last_name: Smith
        - first_name: Joe
          last_name: Sixpack
        - first_name: Jane
          last_name: Doe
    """)[1:]

    it_handles_sequence_of_map_3_item__test_sanity = None
    it_handles_sequence_of_map_3_item__test_pureyaml_pyyaml = [  # :off
        {'first_name': 'John', 'last_name': 'Smith'},
        {'first_name': 'Joe', 'last_name': 'Sixpack'},
        {'first_name': 'Jane', 'last_name': 'Doe'}
    ]  # :on
    it_handles_sequence_of_map_3_item__test_parser = Docs(Doc(Sequence(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_sequence_of_sequences_1_item__data = dedent("""
        - - John Smith
    """)[1:]

    it_handles_sequence_of_sequences_1_item__test_sanity = None
    it_handles_sequence_of_sequences_1_item__test_pureyaml_pyyaml = [  # :off
        ['John Smith']
    ]  # :on
    it_handles_sequence_of_sequences_1_item__test_parser = Docs(Doc(Sequence(  # :off
        Sequence(
            Str('John Smith'),
        ),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_sequence_of_sequences_3_items__data = dedent("""
        - - John Smith
          - Joe Sixpack
          - Jane Doe
    """)[1:]

    it_handles_sequence_of_sequences_3_items__test_sanity = None
    it_handles_sequence_of_sequences_3_items__test_pureyaml_pyyaml = [['John Smith', 'Joe Sixpack', 'Jane Doe']]
    it_handles_sequence_of_sequences_3_items__test_parser = Docs(Doc(Sequence(  # :off
        Sequence(
            Str('John Smith'),
            Str('Joe Sixpack'),
            Str('Jane Doe'),
        ),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_sequence_of_mixed_items__data = dedent("""
        - - John Smith
          - Joe Sixpack
          - Jane Doe
        - Casablanca
        -
          hello: world
          foo: bar
          1 edge case: success
    """)[1:]

    it_handles_sequence_of_mixed_items__test_sanity = None
    it_handles_sequence_of_mixed_items__test_pureyaml_pyyaml = [  # :off
        ['John Smith', 'Joe Sixpack', 'Jane Doe'],
        'Casablanca',
        {
            '1 edge case': 'success',
            'hello': 'world',
            'foo': 'bar'
        }
    ]  # :on
    it_handles_sequence_of_mixed_items__test_parser = Docs(Doc(Sequence(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_of_sequences_1_item__data = dedent("""
        people:
          - John Smith
    """)[1:]

    it_handles_map_of_sequences_1_item__test_sanity = None
    it_handles_map_of_sequences_1_item__test_pureyaml_pyyaml = {'people': ['John Smith']}
    it_handles_map_of_sequences_1_item__test_parser = Docs(Doc(Map(  # :off
        (Str('people'), Sequence(
            Str('John Smith'),
        )),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_of_sequences_many_items__data = dedent("""
        people:
          - John Smith
          - Joe Sixpack
          - Jane Doe
        places:
          - London
          - Australia
          - US

    """)[1:]

    it_handles_map_of_sequences_many_items__test_sanity = None
    it_handles_map_of_sequences_many_items__test_pureyaml_pyyaml = {  # :off
        'people': ['John Smith', 'Joe Sixpack', 'Jane Doe'],
        'places': ['London', 'Australia', 'US']
    }  # :on
    it_handles_map_of_sequences_many_items__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_of_map_1_item__data = dedent("""
        customer:
            first_name:   Dorothy
            family_name:  Gale
    """)[1:]

    it_handles_map_of_map_1_item__test_sanity = None

    it_handles_map_of_map_1_item__test_pureyaml_pyyaml = {  # :off
        'customer': {
            'family_name': 'Gale',
            'first_name': 'Dorothy'
        }
    }  # :on
    it_handles_map_of_map_1_item__test_parser = Docs(Doc(Map(  # :off
        (
            Str('customer'),
            Map(
                (Str('first_name'), Str('Dorothy')),
                (Str('family_name'), Str('Gale')),
            )
        ),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_of_map_many_items__data = dedent("""
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

    it_handles_map_of_map_many_items__test_sanity = None
    it_handles_map_of_map_many_items__test_pureyaml_pyyaml = {
        'customer': {'family_name': 'Gale', 'first_name': 'Dorothy'},
        'cashier': {'family_name': 'Sixpack', 'first_name': 'Joe'},
        'items': ['doritos', 'soda', 'candy'],
        'total': 20
    }
    it_handles_map_of_map_many_items__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_1_item_flow_sequence__data = dedent("""
        --- # Shopping list
        [milk]
    """)[1:]

    it_handles_1_item_flow_sequence__test_sanity = None
    it_handles_1_item_flow_sequence__test_pureyaml_pyyaml = ['milk']
    it_handles_1_item_flow_sequence__test_parser = Docs(Doc(Sequence(  # :off
        Str('milk'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_many_item_flow_sequence__data = dedent("""
        --- # Shopping list
        [milk, pumpkin pie, eggs, juice]
    """)[1:]

    it_handles_many_item_flow_sequence__test_sanity = None
    it_handles_many_item_flow_sequence__test_pureyaml_pyyaml = ['milk', 'pumpkin pie', 'eggs', 'juice']
    it_handles_many_item_flow_sequence__test_parser = Docs(Doc(Sequence(  # :off
        Str('milk'),
        Str('pumpkin pie'),
        Str('eggs'),
        Str('juice'),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_1_item_flow_map__data = dedent("""
        --- # Inline Block
        {name: John Smith}
    """)[1:]

    it_handles_1_item_flow_map__test_sanity = None

    it_handles_1_item_flow_map__test_pureyaml_pyyaml = {'name': 'John Smith'}
    it_handles_1_item_flow_map__test_parser = Docs(Doc(Map(  # :off
        (Str('name'), Str('John Smith')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_2_item_flow_map__data = dedent("""
        --- # Inline Block
        {name: John Smith, age: 33}
    """)[1:]

    it_handles_2_item_flow_map__test_sanity = None

    it_handles_2_item_flow_map__test_pureyaml_pyyaml = {'age': 33, 'name': 'John Smith'}
    it_handles_2_item_flow_map__test_parser = Docs(Doc(Map(  # :off
        (Str('name'), Str('John Smith')),
        (Str('age'), Int(33)),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_mixed_sequence_of_maps__data = dedent("""
        - {name: John Smith, age: 33}
        - name: Mary Smith
          age: 27
    """)[1:]

    it_handles_mixed_sequence_of_maps__test_sanity = None
    it_handles_mixed_sequence_of_maps__test_pureyaml_pyyaml = [{'age': 33, 'name': 'John Smith'},
                                                               {'age': 27, 'name': 'Mary Smith'}]
    it_handles_mixed_sequence_of_maps__test_parser = Docs(Doc(Sequence(  # :off
        Map(
            (Str('name'), Str('John Smith')),
            (Str('age'), Int(33)),
        ),
        Map(
            (Str('name'), Str('Mary Smith')),
            (Str('age'), Int(27)),
        ),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_mixed_map_of_sequences__data = dedent("""
        men: [John Smith, Bill Jones]
        women:
          - Mary Smith
          - Susan Williams
    """)[1:]

    it_handles_mixed_map_of_sequences__test_sanity = None
    it_handles_mixed_map_of_sequences__test_pureyaml_pyyaml = {  # :off
        'women': ['Mary Smith', 'Susan Williams'],
        'men': ['John Smith', 'Bill Jones']
    }  # :on
    it_handles_mixed_map_of_sequences__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_map_of_sequences_with_no_indent__data = dedent(u"""
        men:
        - John Smith
        - Bill Jones
        women:
        - Mary Smith
        - Susan Williams
    """)[1:]

    it_handles_map_of_sequences_with_no_indent__test_sanity = None
    it_handles_map_of_sequences_with_no_indent__test_pureyaml_pyyaml = {  # :off
        'women': ['Mary Smith', 'Susan Williams'],
        'men': ['John Smith', 'Bill Jones']
    }  # :on
    it_handles_map_of_sequences_with_no_indent__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    # noinspection SpellCheckingInspection
    it_handles_cast_type_binary__data = dedent("""
        ---
        picture: !!binary |
            R0lGODlhDAAMAIQAAP//9/X
            17unp5WZmZgAAAOfn515eXv
            Pz7Y6OjuDg4J+fn5OTk6enp
            56enmleECcgggoBADs=mZmE
    """)[1:]

    it_handles_cast_type_binary__test_pureyaml_pyyaml = {  # :off
        'picture': (
            b"GIF89a\x0c\x00\x0c\x00\x84\x00\x00\xff\xff\xf7\xf5\xf5\xee\xe9"
            b"\xe9\xe5fff\x00\x00\x00\xe7\xe7\xe7^^^\xf3\xf3\xed\x8e\x8e\x8e"
            b"\xe0\xe0\xe0\x9f\x9f\x9f\x93\x93\x93\xa7\xa7\xa7\x9e\x9e\x9ei^"
            b"\x10' \x82\n\x01\x00;"
        )
    }  # :on
    it_handles_cast_type_binary__test_sanity = None
    # noinspection SpellCheckingInspection
    it_handles_cast_type_binary__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    # Not supported by PyYaml
    it_handles_1_item_map_explicit_key__data = dedent("""
        ? Hello: World
    """)[1:]

    it_handles_1_item_map_explicit_key__test_pureyaml = {'Hello': 'World'}
    it_handles_1_item_map_explicit_key__test_pyyaml_sanity__skip = None
    it_handles_1_item_map_explicit_key__test_parser = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    # Not supported by PyYaml
    it_handles_2_item_map_explicit_key__data = dedent("""
        ? Hello
        : World
        ? Foo
        : Bar
    """)[1:]

    # Not supported by PyYaml
    it_handles_2_item_map_explicit_key__test_sanity = None
    it_handles_2_item_map_explicit_key__test_pureyaml_pyyaml = {'Foo': 'Bar', 'Hello': 'World'}
    it_handles_2_item_map_explicit_key__test_parser = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    # Not supported by PyYaml
    it_handles_3_item_map_explicit_key__data = dedent("""
        ? Hello
        : World
        ? Foo
        : Bar
        ? More
        : Map Items
    """)[1:]

    it_handles_3_item_map_explicit_key__test_sanity = None
    it_handles_3_item_map_explicit_key__test_pureyaml_pyyaml = {
        'Foo': 'Bar', 'Hello': 'World', 'More': 'Map Items'
    }
    it_handles_3_item_map_explicit_key__test_parser = Docs(Doc(Map(  # :off
        (Str('Hello'), Str('World')),
        (Str('Foo'), Str('Bar')),
        (Str('More'), Str('Map Items')),
    )))  # :on

    # TEST CASE
    # ------------------------------------------------------------------------
    # Not supported by PyYaml
    it_handles_map_complex_key_expanded__data = dedent("""
        ?
          - Detroit Tigers
          - Chicago Cubs
        :
          - 2001-07-23
    """)[1:]

    it_handles_map_complex_key_expanded__test_pureyaml_pyyaml_sanity__skip = None
    it_handles_map_complex_key_expanded__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    # Not supported by PyYaml
    it_handles_map_complex_key_compact__data = dedent("""
        ? - Detroit Tigers
          - Chicago Cubs
        : - 2001-07-23
    """)[1:]

    it_handles_map_complex_key_compact__test_pureyaml_pyyaml_sanity__skip = None
    it_handles_map_complex_key_compact__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    # Not supported by PyYaml
    it_handles_map_complex_key_flow_sequence__data = dedent("""
        ? [ New York Yankees,
            Atlanta Braves ]
        : [ 2001-07-02, 2001-08-12,
            2001-08-14 ]
    """)[1:]

    it_handles_map_complex_key_flow_sequence__test_pureyaml_pyyaml_sanity__skip = None
    it_handles_map_complex_key_flow_sequence__test_parser = Docs(Doc(Map(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_double_dedent__data = dedent("""
        people:
            John Smith:
                nickname: Ol' johnny boy
        places:
            US:
                capital: DC
    """)[1:]

    it_handles_double_dedent__test_pureyaml_pyyaml = {  # :off
        'people': {
            'John Smith': {'nickname': "Ol' johnny boy"}
        },
        'places': {
            'US': {'capital': 'DC'}
        }
    }  # :on
    it_handles_double_dedent__test_sanity = None
    it_handles_double_dedent__test_parser = Docs(Doc(  # :off
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

    # TEST CASE
    # ------------------------------------------------------------------------
    it_handles_double_dedent_with_literal_end__data = dedent("""
        people:
            John Smith:
                short bio: >
                    I like turtles.
                    And green turtles.
                long bio: |
                    I like turtles.
                    And green turtles.
        places:
            US:
                capital: DC
    """)[1:]

    it_handles_double_dedent_with_literal_end__test_pureyaml_pyyaml = {  # :off
        'people': {
            'John Smith': {
                'short bio': 'I like turtles. And green turtles.\n',
                'long bio': 'I like turtles.\nAnd green turtles.\n'
            }
        },
        'places': {
            'US': {'capital': 'DC'}
        }
    }  # :on
    it_handles_double_dedent_with_literal_end__test_sanity = None
    it_handles_double_dedent_with_literal_end__test_parser = Docs(Doc(  # :off
        Map(
            (
                Str('people'),
                Map(
                    (
                        Str('John Smith'),
                        Map(
                            (Str('short bio'), Str('I like turtles. And green turtles.\n')),
                            (Str('long bio'), Str('I like turtles.\nAnd green turtles.\n')),
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

    #  TEST CASE
    # ------------------------------------------------------------------------
    it_handles_nested_map__data = dedent("""
        '1':
          '2': 3
        '4':
          5:
          - '6':
            - 7
            - 8
          - '9': 10
    """)[1:]

    it_handles_nested_map__test_pyyaml = {  # :off
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
    it_handles_nested_map__test_pureyaml_sanity = {  # :off
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
    it_handles_nested_map__test_parser = Docs(Doc(Map(  # :off
        (
            Str(1),
            Map((Str(2), Int(3)))
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
                                Sequence(Int(7), Int(8))
                            )
                        ),
                        Map(
                            (Str(9), Int(10))
                        )
                    )
                )
            )
        )
    )))  # :on
    #  TEST CASE
    # ------------------------------------------------------------------------
    it_handles_sequence_of_map_with_compact_key__data = dedent("""
        - '6':
          - 7
          - 8
        - '9': 10
    """)[1:]

    it_handles_sequence_of_map_with_compact_key__test_sanity = None
    it_handles_sequence_of_map_with_compact_key__test_pyyaml_pureyaml = [  # :off
        {'6': [7, 8]},
        {'9': 10}
    ]  # :on
    it_handles_sequence_of_map_with_compact_key__test_parser = Docs(Doc(Sequence(  # :off
        Map(
            (
                Str(6),
                Sequence(Int(7), Int(8))
            )
        ),
        Map(
            (Str(9), Int(10))
        )
    )))  # :on
    #  TEST CASE
    # ------------------------------------------------------------------------
    it_handles_deeply_nested_object__data = dedent("""
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

    it_handles_deeply_nested_object__test_sanity = None
    it_handles_deeply_nested_object__test_pyyaml_pureyaml = {  # :off
        '4': {
            16: 17,
            5: {
                '10': 11,
                '12': {
                    '13': {'14': '15'}
                },
                '8': 9,
                '6': 7
            }
        },
        '1': {'2': 3}
    }  # :on
    it_handles_deeply_nested_object__test_parser = Docs(Doc(Map(  # :off
        (
            Str('4'),
            Map(
                (Int(16), Int(17)),
                (
                    Int(5),
                    Map(
                        (Str('10'), Int(11)),
                        (
                            Str('12'),
                            Map(
                                (
                                    Str('13'),
                                    Map(
                                        (Str('14'), Str('15')),
                                    ),
                                ),
                            ),
                        ),
                        (Str('8'), Int(9)),
                        (Str('6'), Int(7)),
                    ),
                ),
            ),
        ),
        (
            Str('1'),
            Map(
                (Str('2'), Int(3)),
            ),
        )
    )))  # :on

    #  TEST CASE
    # ------------------------------------------------------------------------

    it_handles_deeply_nested_list__data = dedent("""
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

    it_handles_deeply_nested_list__test_sanity = None
    it_handles_deeply_nested_list__test_pyyaml_pureyaml = [  # :off
        1,
        [
            [2, 3],
            [
                4,
                [5, 6]
            ],
            7
        ],
        [8, 9, 10],
        [
            [11, 12],
            [13, 14, 15, 16]
        ]
    ]  # :on
    it_handles_deeply_nested_list__test_parser = Docs(Doc(Sequence(  # :off
        Int(1),
        Sequence(
            Sequence(
                Int(2),
                Int(3),
            ),
            Sequence(
                Int(4),
                Sequence(
                    Int(5),
                    Int(6),
                ),
            ),
            Int(7),
        ),
        Sequence(
            Int(8),
            Int(9),
            Int(10),
        ),
        Sequence(
            Sequence(
                Int(11),
                Int(12),
            ),
            Sequence(
                Int(13),
                Int(14),
                Int(15),
                Int(16),
            ),
        ),
    )))  # :on


pureyaml_parser = YAMLParser(debug=True)


@mark.parametrize('case', DecoderTestCase.keys('parser'))
def test_parser(case):
    text, expected = DecoderTestCase.get('parser', case)
    nodes = pureyaml_parser.parse(text)
    # print(serialize_nodes(nodes))
    assert nodes == expected


@mark.parametrize('case', DecoderTestCase.keys('pureyaml'))
def test_pureyaml_load(case):
    text, expected = DecoderTestCase.get('pureyaml', case)
    obj = pureyaml.load(text)
    # print('\n' + str(obj))
    assert obj == expected


@mark.parametrize('case', DecoderTestCase.keys('pyyaml'))
def test_pyyaml_load(case):
    text, expected = DecoderTestCase.get('pyyaml', case)
    obj = pyyaml.load(text)
    # print('{case}__test_pureyaml_pyyaml_sanity={obj!r}'.format(case=case, obj=obj))
    assert obj == expected


@mark.parametrize('case', DecoderTestCase.keys('sanity'))
def test_sanity(case):
    text, _ = DecoderTestCase.get('sanity', case)
    obj1 = pureyaml.load(text)
    # print(obj1)
    _text = pureyaml.dump(obj1)
    # print(_text)
    obj2 = pureyaml.load(_text)
    # print(obj2)
    assert obj1 == obj2
