#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import serialize_nodes

pureyaml_parser = YAMLParser(debug=True)



def test_example_5_1__byte_order_mark():
    """Example 5.1. Byte Order Mark"""

    text = dedent("""
         # Comment only.
    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_2__invalid_byte_order_mark():
    """Example 5.2. Invalid Byte Order Mark"""

    text = dedent("""
        - Invalid use of BOM

        - Inside a document.

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Sequence(
                Str('Invalid use of BOM'),
                Str('Inside a document.'),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_3__block_structure_indicators():
    """Example 5.3. Block Structure Indicators"""

    text = dedent("""
        sequence:
        - one
        - two
        mapping:
          ? sky
          : blue
          sea : green

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('sequence'),
                    Sequence(
                        Str('one'),
                        Str('two'),
                    ),
                ),
                (
                    Str('mapping'),
                    Map(
                        (Str('sky'), Str('blue')),
                        (Str('sea'), Str('green')),
                    ),
                ),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_4__flow_collection_indicators():
    """Example 5.4. Flow Collection Indicators"""

    text = dedent("""
        sequence: [ one, two, ]
        mapping: { sky: blue, sea: green }

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('sequence'),
                    Sequence(
                        Str('one'),
                        Str('two'),
                    ),
                ),
                (
                    Str('mapping'),
                    Map(
                        (Str('sky'), Str('blue')),
                        (Str('sea'), Str('green')),
                    ),
                ),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_5__comment_indicator():
    """Example 5.5. Comment Indicator"""

    text = dedent("""
        # Comment only.
    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_6__node_property_indicators():
    """Example 5.6. Node Property Indicators"""

    text = dedent("""
        anchored: !local &
        anchor value
        alias: *anchor

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_7__block_scalar_indicators():
    """Example 5.7. Block Scalar Indicators"""

    text = dedent("""
        literal: |
          some
          text
        folded: >
          some
          text

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('literal'), Str('some\ntext\n')),
                (Str('folded'), Str('some text\n')),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_8__quoted_scalar_indicators():
    """Example 5.8. Quoted Scalar Indicators"""

    text = dedent("""
        single: 'text'
        double: "text"

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('single'), Str('text')),
                (Str('double'), Str('text')),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_9__directive_indicator():
    """Example 5.9. Directive Indicator"""

    text = dedent("""
        %YAML 1.2
        --- text

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('text'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_10__invalid_use_of_reserved_indicators():
    """Example 5.10. Invalid use of Reserved Indicators"""

    text = dedent("""
        commercial-at: @text
        grave-accent: `text

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('commercial-at'), Str('@text')),
                (Str('grave-accent'), Str('`text')),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_11__line_break_characters():
    """Example 5.11. Line Break Characters"""

    text = dedent("""
        |
          Line break (no glyph)
          Line break (glyphed)

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_12__tabs_and_spaces():
    """Example 5.12. Tabs and Spaces"""

    text = dedent("""
        # Tabs and spaces
        quoted: "Quoted  "
        block: |
          void main() {
           printf("Hello, world!\n");
          }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_13__escaped_characters():
    """Example 5.13. Escaped Characters"""

    text = dedent(r"""
        "Fun with \\
        \" \a \b \e \f \
        \n \r \t \v \0 \
        \  \_ \N \L \P \
        \x41 \u0041 \U00000041"

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('Fun with \\\\\n" \\a \\b \\e \\f \\\n\\n \\r \\t \\v \\0 \\\n\\  \\_ \\N \\L \\P \\\n\\x41 \\u0041 '
                '\\U00000041'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_5_14__invalid_escaped_characters():
    """Example 5.14. Invalid Escaped Characters"""

    text = dedent(r"""
        Bad escapes:  "\c
          \xq-"

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('Bad escapes'), Str('\\c \\xq-')),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_1__indentation_spaces():
    """Example 6.1. Indentation Spaces"""

    text = dedent("""
          # Leading comment line spaces are
           # neither content nor indentation.

        Not indented:
         By one space: |
            By four
              spaces
         Flow style: [    # Leading spaces
           By two,        # in flow style
          Also by two,    # are neither
           Still by two   # content nor
            ]             # indentation.

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_2__indentation_indicators():
    """Example 6.2. Indentation Indicators"""

    text = dedent("""
        ? a: - b
          -  - c
             - d

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_3__separation_spaces():
    """Example 6.3. Separation Spaces"""

    text = dedent("""
        - foo:  bar- - baz
          - baz

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_4__line_prefixes():
    """Example 6.4. Line Prefixes"""

    text = dedent("""
        plain: text  lines
        quoted: "text
           lines"
        block: |
          text
            lines

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('text  lines')),
                (Str('quoted'), Str('text lines')),
                (Str('block'), Str('text\n  lines\n')),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_5__empty_lines():
    """Example 6.5. Empty Lines"""

    text = dedent("""
        Folding:  "Empty line

          as a line feed"
        Chomping: |
          Clipped empty lines


    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('Folding'), Str('Empty line as a line feed')),
                (Str('Chomping'), Str('Clipped empty lines\n')),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_6__line_folding():
    """Example 6.6. Line Folding"""

    text = dedent("""
        >-
          trimmed



          as
          space

    """)[1:-1]

    expected = None
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_7__block_folding():
    """Example 6.7. Block Folding"""

    text = dedent("""
        >
          foo

            bar

          baz

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('foo\n  bar\nbaz\n'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_8__flow_folding():
    """Example 6.8. Flow Folding"""

    text = dedent("""
        "
          foo

            bar

          baz
        "

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str(' foo bar baz\n'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_9__separated_comment():
    """Example 6.9. Separated Comment"""

    text = dedent("""
        key:    # Comment   valueeof

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_10__comment_lines():
    """Example 6.10. Comment Lines"""

    text = dedent("""
          # Comment


    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_11__multi_line_comments():
    """Example 6.11. Multi-Line Comments"""

    text = dedent("""
        key:    # Comment
                # lines
          value


    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_12__separation_spaces():
    """Example 6.12. Separation Spaces"""

    text = dedent("""
        { first: Sammy, last: Sosa }: # Statistics:
          hr:  # Home runs
             65
          avg: # Average
           0.278

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_13__reserved_directives():
    """Example 6.13. Reserved Directives"""

    text = dedent("""
        %FOO  bar baz # Should be ignored               # with a warning.
        --- "foo"

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('"foo"'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_14__yaml__directive():
    """Example 6.14. “ YAML ” directive"""

    text = dedent("""
        %YAML 1.3 # Attempt parsing           # with a warning
        ---
        "foo"

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('foo'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_15__invalid_repeated_yaml_directive():
    """Example 6.15. Invalid Repeated YAML directive"""

    text = dedent("""
        %YAML 1.2%YAML 1.1
        foo

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('foo'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_16__tag__directive():
    """Example 6.16. “ TAG ” directive"""

    text = dedent("""
        %TAG !yaml! tag:yaml.org,2002:---
        !yaml!str "foo"

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_17__invalid_repeated_tag_directive():
    """Example 6.17. Invalid Repeated TAG directive"""

    text = dedent("""
        %TAG ! !foo%TAG ! !foo
        bar

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('bar'),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_18__primary_tag_handle():
    """Example 6.18. Primary Tag Handle"""

    text = dedent("""
        # Private
        !foo "bar"
        ...
        # Global
        %TAG ! tag:example.com,2000:app/
        ---
        !foo "bar"

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_19__secondary_tag_handle():
    """Example 6.19. Secondary Tag Handle"""

    text = dedent("""
        %TAG !! tag:example.com,2000:app/---
        !!int 1 - 3 # Interval, not integer

    """)[1:-1]

    expected = Docs(  # :off
        Doc(
            Str('%TAG !! tag:example.com,2000:app/--'),
        ),
        Doc(
            Sequence(
                Int(1),
                Int(3),
            ),
        ),
    )  # :on
    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_20__tag_handles():
    """Example 6.20. Tag Handles"""

    text = dedent("""
        %TAG !e! tag:example.com,2000:app/---
        !e!foo "bar"

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_21__local_tag_prefix():
    """Example 6.21. Local Tag Prefix"""

    text = dedent("""
        %TAG !m! !my
        ---- # Bulb here
        !m!light fluorescent
        ...
        %TAG !m! !my-
        --- # Color here
        !m!light green

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_22__global_tag_prefix():
    """Example 6.22. Global Tag Prefix"""

    text = dedent("""
        %TAG !e! tag:example.com,2000:app/
        ---
        - !e!foo "bar"

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_23__node_properties():
    """Example 6.23. Node Properties"""

    text = dedent("""
        !!str &a1 "foo":  !!str bar
        &a2 baz : *a1

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_24__verbatim_tags():
    """Example 6.24. Verbatim Tags"""

    text = dedent("""
        !<tag:yaml.org,2002:str> foo :  !<!bar> baz

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_25__invalid_verbatim_tags():
    """Example 6.25. Invalid Verbatim Tags"""

    text = dedent("""
        - !<!> foo
        - !<$:?> bar

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_26__tag_shorthands():
    """Example 6.26. Tag Shorthands"""

    text = dedent("""
        %TAG !e! tag:example.com,2000:app/
        ---
        - !local foo
        - !!str bar
        - !e!tag%21 baz

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_27__invalid_tag_shorthands():
    """Example 6.27. Invalid Tag Shorthands"""

    text = dedent("""
        %TAG !e! tag:example,2000:app/
        ---
        - !e! foo
        - !h!bar baz

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_28__non_specific_tags():
    """Example 6.28. Non-Specific Tags"""

    text = dedent("""
        # Assuming conventional resolution:- "12"
        - 12
        - ! 12

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_6_29__node_anchors():
    """Example 6.29. Node Anchors"""

    text = dedent("""
        First occurrence: &anchor ValueSecond occurrence: *anchor

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_1__alias_nodes():
    """Example 7.1. Alias Nodes"""

    text = dedent("""
        First occurrence: &anchor FooSecond occurrence: *anchor
        Override anchor: &anchor Bar
        Reuse anchor: *anchor

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_2__empty_content():
    """Example 7.2. Empty Content"""

    text = dedent("""
        {  foo : !!str ,
          !!str  : bar,
        }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_3__completely_empty_flow_nodes():
    """Example 7.3. Completely Empty Flow Nodes"""

    text = dedent("""
        {  ? foo : ,
           : bar,
        }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_4__double_quoted_implicit_keys():
    """Example 7.4. Double Quoted Implicit Keys"""

    text = dedent("""
        "implicit block key" : [  "implicit flow key" : value,
         ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_5__double_quoted_line_breaks():
    """Example 7.5. Double Quoted Line Breaks"""

    text = dedent("""
        "folded  to a space,

        to a line feed, or  \
         \  non-content"

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_6__double_quoted_lines():
    """Example 7.6. Double Quoted Lines"""

    text = dedent("""
        " 1st non-empty
         2nd non-empty
         3rd non-empty "

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_7__single_quoted_characters():
    """Example 7.7. Single Quoted Characters"""

    text = dedent("""
         'here''s to "quotes"'
    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_8__single_quoted_implicit_keys():
    """Example 7.8. Single Quoted Implicit Keys"""

    text = dedent("""
        'implicit block key' : [  'implicit flow key' : value,
         ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_9__single_quoted_lines():
    """Example 7.9. Single Quoted Lines"""

    text = dedent("""
        ' 1st non-empty
         2nd non-empty
         3rd non-empty '

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_10__plain_characters():
    """Example 7.10. Plain Characters"""

    text = dedent("""
        # Outside flow collection:- ::vector
        - ": - ()"
        - Up, up, and away!
        - -123
        - http://example.com/foo#bar
        # Inside flow collection:
        - [ ::vector,
          ": - ()",
          "Up, up and away!",
          -123,
          http://example.com/foo#bar ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_11__plain_implicit_keys():
    """Example 7.11. Plain Implicit Keys"""

    text = dedent("""
        implicit block key : [  implicit flow key : value,
         ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_12__plain_lines():
    """Example 7.12. Plain Lines"""

    text = dedent("""
        1st non-empty
         2nd non-empty
         3rd non-empty

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_13__flow_sequence():
    """Example 7.13. Flow Sequence"""

    text = dedent("""
        - [ one, two, ]- [three ,four]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_14__flow_sequence_entries():
    """Example 7.14. Flow Sequence Entries"""

    text = dedent("""
        [
        "double
         quoted", 'single
                   quoted',
        plain
         text, [ nested ],
        single: pair,
        ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_15__flow_mappings():
    """Example 7.15. Flow Mappings"""

    text = dedent("""
        - { one : two , three: four , }- {five: six,seven : eight}

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_16__flow_mapping_entries():
    """Example 7.16. Flow Mapping Entries"""

    text = dedent("""
        {? explicit: entry,
        implicit: entry,
        ?
        }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_17__flow_mapping_separate_values():
    """Example 7.17. Flow Mapping Separate Values"""

    text = dedent("""
        {
        unquoted : "separate",
        http://foo.com,
        omitted value: ,
         : omitted key,
        }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_18__flow_mapping_adjacent_values():
    """Example 7.18. Flow Mapping Adjacent Values"""

    text = dedent("""
        {
        "adjacent":value,
        "readable": value,
        "empty":
        }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_19__single_pair_flow_mappings():
    """Example 7.19. Single Pair Flow Mappings"""

    text = dedent("""
        [
        foo: bar
        ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_20__single_pair_explicit_entry():
    """Example 7.20. Single Pair Explicit Entry"""

    text = dedent("""
        [? foo
         bar : baz
        ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_21__single_pair_implicit_entries():
    """Example 7.21. Single Pair Implicit Entries"""

    text = dedent("""
        - [ YAML : separate ]- [  : empty key entry ]
        - [ {JSON: like}:adjacent ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_22__invalid_implicit_keys():
    """Example 7.22. Invalid Implicit Keys"""

    text = dedent("""
        [ foo bar: invalid,
         "foo...>1K characters...bar": invalid ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_23__flow_content():
    """Example 7.23. Flow Content"""

    text = dedent("""
        - [ a, b ]- { a: b }
        - "a"
        - 'b'
        - c

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_7_24__flow_nodes():
    """Example 7.24. Flow Nodes"""

    text = dedent("""
        - !!str "a"- 'b'
        - &anchor "c"
        - *anchor
        - !!str

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_1__block_scalar_header():
    """Example 8.1. Block Scalar Header"""

    text = dedent("""
        - | # Empty header  literal
        - >1 # Indentation indicator
          folded
        - |+ # Chomping indicator
         keep

        - >1- # Both indicators
          strip


    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_2__block_indentation_indicator():
    """Example 8.2. Block Indentation Indicator"""

    text = dedent("""
        - |
         detected
        - >


          # detected
        - |1
          explicit
        - >

         detected

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_3__invalid_block_scalar_indentation_indicators():
    """Example 8.3. Invalid Block Scalar Indentation Indicators"""

    text = dedent("""
        - |
         text
        - >
          text
         text
        - |2
         text

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_4__chomping_final_line_break():
    """Example 8.4. Chomping Final Line Break"""

    text = dedent("""
        strip: |-  text
        clip: |
          text
        keep: |+
          text

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_5__chomping_trailing_lines():
    """Example 8.5. Chomping Trailing Lines"""

    text = dedent("""
         # Strip  # Comments:
        strip: |-
          # text

         # Clip
          # comments:

        clip: |
          # text

         # Keep
          # comments:

        keep: |+
          # text

         # Trail
          # comments.

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_6__empty_scalar_chomping():
    """Example 8.6. Empty Scalar Chomping"""

    text = dedent("""
        strip: >-

        clip: >

        keep: |+


    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_7__literal_scalar():
    """Example 8.7. Literal Scalar"""

    text = dedent("""
        |  literal
          text


    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_8__literal_content():
    """Example 8.8. Literal Content"""

    text = dedent("""
        |


          literal


          text

         # Comment

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_9__folded_scalar():
    """Example 8.9. Folded Scalar"""

    text = dedent("""
        >  folded
         text


    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_10__folded_lines():
    """Example 8.10. Folded Lines"""

    text = dedent("""
        >
         folded
         line

         next
         line
           * bullet

           * list
           * lines

         last
         line

        # Comment

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_11__more_indented_lines():
    """Example 8.11. More Indented Lines"""

    text = dedent("""
        >
         folded
         line

         next
         line
           * bullet

           * list
           * lines

         last
         line

        # Comment

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_12__empty_separation_lines():
    """Example 8.12. Empty Separation Lines"""

    text = dedent("""
        >

         folded
         line

         next
         line
           * bullet

           * list
           * line

         last
         line

        # Comment

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_13__final_empty_lines():
    """Example 8.13. Final Empty Lines"""

    text = dedent("""
        > folded
         line

         next
         line
           * bullet

           * list
           * line

         last
         line

        # Comment

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_14__block_sequence():
    """Example 8.14. Block Sequence"""

    text = dedent("""
        block sequence:  - one
          - two : three

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_15__block_sequence_entry_types():
    """Example 8.15. Block Sequence Entry Types"""

    text = dedent("""
        -  # Empty- |
         block node
        - - one # Compact
          - two # sequence
        - one: two # Compact mapping

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_16__block_mappings():
    """Example 8.16. Block Mappings"""

    text = dedent("""
        block mapping:
         key: value

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_17__explicit_block_mapping_entries():
    """Example 8.17. Explicit Block Mapping Entries"""

    text = dedent("""
        ? explicit key # Empty value
        ? |
          block key
        : - one # Explicit compact
          - two # block value

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_18__implicit_block_mapping_entries():
    """Example 8.18. Implicit Block Mapping Entries"""

    text = dedent("""
        plain key: in-line value
         :  # Both empty
        "quoted key":
        - entry

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_19__compact_block_mappings():
    """Example 8.19. Compact Block Mappings"""

    text = dedent("""
        - sun: yellow - ? earth: blue
          : moon: white

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_20__block_node_types():
    """Example 8.20. Block Node Types"""

    text = dedent("""
        -   "flow in block"
        - >
         Block scalar
        - !!map # Block collection
          foo : bar

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_21__block_scalar_nodes():
    """Example 8.21. Block Scalar Nodes"""

    text = dedent("""
        literal: |2  value
        folded:
           !foo
          >1
         value

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_8_22__block_collection_nodes():
    """Example 8.22. Block Collection Nodes"""

    text = dedent("""
        sequence: !!seq
        - entry
        - !!seq
         - nested
        mapping: !!map
         foo: bar

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_9_1__document_prefix():
    """Example 9.1. Document Prefix"""

    text = dedent("""
         # Comment# lines
        Document

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_9_2__document_markers():
    """Example 9.2. Document Markers"""

    text = dedent("""
        %YAML 1.2
        ---
        Document
        ... # Suffix

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_9_3__bare_documents():
    """Example 9.3. Bare Documents"""

    text = dedent("""
        Baredocument
        ...
        # No document
        ...
        |
        %!PS-Adobe-2.0 # Not the first line

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_9_4__explicit_documents():
    """Example 9.4. Explicit Documents"""

    text = dedent("""
        ---{ matches
        % : 20 }
        ...
        ---
        # Empty
        ...

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_9_5__directives_documents():
    """Example 9.5. Directives Documents"""

    text = dedent("""
        %YAML 1.2--- |
        %!PS-Adobe-2.0
        ...
        %YAML1.2
        ---
        # Empty
        ...

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_9_6__stream():
    """Example 9.6. Stream"""

    text = dedent("""
        Document
        ---
        # Empty
        ...
        %YAML 1.2
        ---
        matches %: 20

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_1__map_examples():
    """Example 10.1. !!map Examples"""

    text = dedent("""
        Block style: !!map  Clark : Evans
          Ingy  : d t Net
          Oren  : Ben-Kiki

        Flow style: !!map { Clark: Evans, Ingy: d t Net, Oren: Ben-Kiki }

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_2__seq_examples():
    """Example 10.2. !!seq Examples"""

    text = dedent("""
        Block style: !!seq- Clark Evans
        - Ingy d t Net
        - Oren Ben-Kiki

        Flow style: !!seq [ Clark Evans, Ingy d t Net, Oren Ben-Kiki ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_3__str_examples():
    """Example 10.3. !!str Examples"""

    text = dedent("""
        Block style: !!str |-  String: just a theory.

        Flow style: !!str "String: just a theory."

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_4__null_examples():
    """Example 10.4. !!null Examples"""

    text = dedent("""
        !!null null: value for null keykey with null value: !!null null

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_5__bool_examples():
    """Example 10.5. !!bool Examples"""

    text = dedent("""
        YAML is a superset of JSON: !!bool truePluto is a planet: !!bool false

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_6__int_examples():
    """Example 10.6. !!int Examples"""

    text = dedent("""
        negative: !!int -12zero: !!int 0
        positive: !!int 34

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_7__float_examples():
    """Example 10.7. !!float Examples"""

    text = dedent("""
        negative: !!float -1zero: !!float 0
        positive: !!float 2.3e4
        infinity: !!float .inf
        not a number: !!float .nan

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_8__json_tag_resolution():
    """Example 10.8. JSON Tag Resolution"""

    text = dedent("""
        A null: nullBooleans: [ true, false ]
        Integers: [ 0, -0, 3, -19 ]
        Floats: [ 0., -0.0, 12e03, -2E+05 ]
        Invalid: [ True, Null, 0o7, 0x3A, +12.3 ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected


def test_example_10_9__core_tag_resolution():
    """Example 10.9. Core Tag Resolution"""

    text = dedent("""
        A null: nullAlso a null: # Empty
        Not a null: ""
        Booleans: [ true, True, false, FALSE ]
        Integers: [ 0, 0o7, 0x3A, -19 ]
        Floats: [ 0., -0.0, .5, +12e03, -2E+05 ]
        Also floats: [ .inf, -.Inf, +.INF, .NAN ]

    """)[1:-1]

    expected = None

    nodes = pureyaml_parser.parse(text)
    print(serialize_nodes(nodes))

    assert nodes == expected
