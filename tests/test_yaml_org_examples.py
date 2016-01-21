#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

from pytest import raises

from pureyaml.exceptions import YAMLSyntaxError
from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import serialize_nodes, feature_not_supported

parser = YAMLParser(debug=True)


def print_nodes(nodes):
    active = True
    if active:
        print(serialize_nodes(nodes))


@feature_not_supported
def test_example_5_1__byte_order_mark():
    """
    Example 5.1. Byte Order Mark

    Expected:
        # This stream contains no
        # documents, only comments.

    """

    text = dedent("""
         # Comment only.
    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_2__invalid_byte_order_mark():
    """
    Example 5.2. Invalid Byte Order Mark

    Expected:
        ERROR:
         A BOM must not appear
         inside a document.

    """

    text = dedent("""
        - Invalid use of BOM

        - Inside a document.

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


def test_example_5_3__block_structure_indicators():
    """
    Example 5.3. Block Structure Indicators

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "sequence"
          : !!seq [ !!str "one", !!str "two" ],
          ? !!str "mapping"
          : !!map {
            ? !!str "sky" : !!str "blue",
            ? !!str "sea" : !!str "green",
          },
        }

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_4__flow_collection_indicators():
    """
    Example 5.4. Flow Collection Indicators

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "sequence"
          : !!seq [ !!str "one", !!str "two" ],
          ? !!str "mapping"
          : !!map {
            ? !!str "sky" : !!str "blue",
            ? !!str "sea" : !!str "green",
          },
        }

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_5_5__comment_indicator():
    """
    Example 5.5. Comment Indicator

    Expected:
        # This stream contains no
        # documents, only comments.

    """

    text = dedent("""
        # Comment only.
    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_5_6__node_property_indicators():
    """
    Example 5.6. Node Property Indicators

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "anchored"
          : !local &A1 "value",
          ? !!str "alias"
          : *A1,
        }

    """

    text = dedent("""
        anchored: !local &anchor value
        alias: *anchor

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_7__block_scalar_indicators():
    """
    Example 5.7. Block Scalar Indicators

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "literal"
          : !!str "some\ntext\n",
          ? !!str "folded"
          : !!str "some text\n",
        }

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_8__quoted_scalar_indicators():
    """
    Example 5.8. Quoted Scalar Indicators

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "single"
          : !!str "text",
          ? !!str "double"
          : !!str "text",
        }

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_9__directive_indicator():
    """
    Example 5.9. Directive Indicator

    Expected:
        %YAML 1.2
        ---
        !!str "text"

    """

    text = dedent("""
        %YAML 1.2
        --- text

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('text'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_10__invalid_use_of_reserved_indicators():
    """
    Example 5.10. Invalid use of Reserved Indicators

    Expected:
        ERROR:
         Reserved indicators can't
         start a plain scalar.

    """

    text = dedent("""
        commercial-at: @text
        grave-accent: `text

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


def test_example_5_11__line_break_characters():
    """
    Example 5.11. Line Break Characters

    Expected:
        %YAML 1.2
        ---
        !!str "line break (no glyph)\n\
              line break (glyphed)\n"

    """

    text = dedent("""
        |
          Line break (no glyph)
          Line break (glyphed)

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('Line break (no glyph)\nLine break (glyphed)\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_12__tabs_and_spaces():
    """
    Example 5.12. Tabs and Spaces

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "quoted"
          : "Quoted \t",
          ? !!str "block"
          : "void main() {\n\
            \tprintf(\"Hello, world!\\n\");\n\
            }\n",
        }

    """

    text = dedent("""
        # Tabs and spaces
        quoted: "Quoted \t"
        block: |
          void main() {
          \tprintf("Hello, world!\n");
          }

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (Str('quoted'), Str('Quoted \t')),
                    (Str('block'), Str('void main() {\n\tprintf("Hello, world!\\n");\n}\n')),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_13__escaped_characters():
    """
    Example 5.13. Escaped Characters

    Expected:
        %YAML 1.2
        ---
        "Fun with \x5C
        \x22 \x07 \x08 \x1B \x0C
        \x0A \x0D \x09 \x0B \x00
        \x20 \xA0 \x85 \u2028 \u2029
        A A A"

    """

    text = dedent(r"""
        "Fun with \\
        \" \a \b \e \f \
        \n \r \t \v \0 \
        \  \_ \N \L \P \
        \x41 \u0041 \U00000041"

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('Fun with \\\\\n" \\a \\b \\e \\f \\ \n\\n \\r \\t \\v '
                    '\\0 \\ \n\\  \\_ \\N \\L \\P \\ \n\\x41 \\u0041 '
                    '\\U00000041'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_5_14__invalid_escaped_characters():
    """
    Example 5.14. Invalid Escaped Characters

    Expected:
        ERROR:
        - c is an invalid escaped character.
        - q and - are invalid hex digits.

    """

    text = dedent(r"""
        Bad escapes:
          "\c
          \xq-"

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


def test_example_6_1__indentation_spaces():
    """
    Example 6.1. Indentation Spaces

    Expected:
        %YAML 1.2
        - - -
        !!map {
          ? !!str "Not indented"
          : !!map {
              ? !!str "By one space"
              : !!str "By four\n  spaces\n",
              ? !!str "Flow style"
              : !!seq [
                  !!str "By two",
                  !!str "Also by two",
                  !!str "Still by two",
                ]
            }
        }

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_2__indentation_indicators():
    """
    Example 6.2. Indentation Indicators

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "a"
          : !!seq [
            !!str "b",
            !!seq [ !!str "c", !!str "d" ]
          ],
        }

    """

    text = dedent("""
        ? a: - b
          -  - c
             - d

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_3__separation_spaces():
    """
    Example 6.3. Separation Spaces

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!map {
            ? !!str "foo" : !!str "bar",
          },
          !!seq [ !!str "baz", !!str "baz" ],
        ]

    """

    text = dedent("""
        - foo:  bar
        - - baz
          - baz

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Map(
                        (Str('foo'), Str('bar')),
                    ),
                    Sequence(
                        Str('baz'),
                        Str('baz'),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_4__line_prefixes():
    """
    Example 6.4. Line Prefixes

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "plain"
          : !!str "text lines",
          ? !!str "quoted"
          : !!str "text lines",
          ? !!str "block"
          : !!str "text\n  lines\n",
        }

    """

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
                    (Str('plain'), Str('text lines')),
                    (Str('quoted'), Str('text lines')),
                    (Str('block'), Str('text\n  lines\n')),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_5__empty_lines():
    """
    Example 6.5. Empty Lines

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "Folding"
          : !!str "Empty line\nas a line feed",
          ? !!str "Chomping"
          : !!str "Clipped empty lines\n",
        }

    """

    text = dedent("""
        Folding:
          "Empty line

          as a line feed"
        Chomping: |
          Clipped empty lines


    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_6__line_folding():
    """
    Example 6.6. Line Folding

    Expected:
        %YAML 1.2
        ---
        !!str "trimmed\n\n\nas space"

    """

    text = dedent("""
        >-
          trimmed



          as
          space

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('trimmed\n\n\nas space'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_7__block_folding():
    """
    Example 6.7. Block Folding

    Expected:
        %YAML 1.2
        --- !!str
        "foo \n\n\t bar\n\nbaz\n"

    """

    text = dedent("""
        >
          foo

          \t bar

          baz

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('foo \n\n\t bar\n\nbaz\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_8__flow_folding():
    """
    Example 6.8. Flow Folding

    Expected:
        %YAML 1.2
        --- !!str
        " foo\nbar\nbaz "

    """

    text = dedent("""
        "
          foo

            bar

          baz
        "

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str(' foo\nbar\nbaz '),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_9__separated_comment():
    """
    Example 6.9. Separated Comment

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "key"
          : !!str "value",
        }

    """

    text = dedent("""
        key:    # Comment
          value

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_10__comment_lines():
    """
    Example 6.10. Comment Lines

    Expected:
        # This stream contains no
        # documents, only comments.

    """

    text = dedent("""
          # Comment


    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_11__multi_line_comments():
    """
    Example 6.11. Multi-Line Comments

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "key"
          : !!str "value",
        }

    """

    text = dedent("""
        key:    # Comment
                # lines
          value


    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_6_12__separation_spaces():
    """
    Example 6.12. Separation Spaces

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!map {
            ? !!str "first"
            : !!str "Sammy",
            ? !!str "last"
            : !!str "Sosa",
          }
          : !!map {
            ? !!str "hr"
            : !!int "65",
            ? !!str "avg"
            : !!float "0.278",
          },
        }

    """

    text = dedent("""
        { first: Sammy, last: Sosa }:
        # Statistics:
          hr:  # Home runs
             65
          avg: # Average
           0.278

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_13__reserved_directives():
    """
    Example 6.13. Reserved Directives

    Expected:
        %YAML 1.2
        --- !!str
        "foo"

    """

    text = dedent("""
        %FOO  bar baz # Should be ignored
                       # with a warning.
        --- "foo"

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_14__yaml__directive():
    """
    Example 6.14. “ YAML ” directive

    Expected:
        %YAML 1.2
        ---
        !!str "foo"

    """

    text = dedent("""
        %YAML 1.3 # Attempt parsing
                   # with a warning
        ---
        "foo"

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_15__invalid_repeated_yaml_directive():
    """
    Example 6.15. Invalid Repeated YAML directive

    Expected:
        ERROR:
        The YAML directive must only be
        given at most once per document.

    """

    text = dedent("""
        %YAML 1.2
        %YAML 1.1
        foo

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


@feature_not_supported
def test_example_6_16__tag__directive():
    """
    Example 6.16. “ TAG ” directive

    Expected:
        %YAML 1.2
        ---
        !!str "foo"

    """

    text = dedent("""
        %TAG !yaml! tag:yaml.org,2002:
        ---
        !yaml!str "foo"

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_17__invalid_repeated_tag_directive():
    """
    Example 6.17. Invalid Repeated TAG directive

    Expected:
        ERROR:
        The TAG directive must only
        be given at most once per
        handle in the same document.

    """

    text = dedent("""
        %TAG ! !foo
        %TAG ! !foo
        bar

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


@feature_not_supported
def test_example_6_18__primary_tag_handle():
    """
    Example 6.18. Primary Tag Handle

    Expected:
        %YAML 1.2
        ---
        !<!foo> "bar"
        ...
        ---
        !<tag:example.com,2000:app/foo> "bar"

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_19__secondary_tag_handle():
    """
    Example 6.19. Secondary Tag Handle

    Expected:
        %YAML 1.2
        ---
        !<tag:example.com,2000:app/int> "1 - 3"

    """

    text = dedent("""
        %TAG !! tag:example.com,2000:app/
        ---
        !!int 1 - 3 # Interval, not integer

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Int(1-3),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_20__tag_handles():
    """
    Example 6.20. Tag Handles

    Expected:
        %YAML 1.2
        ---
        !<tag:example.com,2000:app/foo> "bar"

    """

    text = dedent("""
        %TAG !e! tag:example.com,2000:app/
        ---
        !e!foo "bar"

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_21__local_tag_prefix():
    """
    Example 6.21. Local Tag Prefix

    Expected:
        %YAML 1.2
        ---
        !<!my-light> "fluorescent"
        ...
        %YAML 1.2
        ---
        !<!my-light> "green"

    """

    text = dedent("""
        %TAG !m! !my-
        --- # Bulb here
        !m!light fluorescent
        ...
        %TAG !m! !my-
        --- # Color here
        !m!light green

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_22__global_tag_prefix():
    """
    Example 6.22. Global Tag Prefix

    Expected:
        %YAML 1.2
        ---
        !<tag:example.com,2000:app/foo> "bar"

    """

    text = dedent("""
        %TAG !e! tag:example.com,2000:app/
        ---
        - !e!foo "bar"

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_23__node_properties():
    """
    Example 6.23. Node Properties

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? &B1 !!str "foo"
          : !!str "bar",
          ? !!str "baz"
          : *B1,
        }

    """

    text = dedent("""
        !!str &a1 "foo":
          !!str bar
        &a2 baz : *a1

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_24__verbatim_tags():
    """
    Example 6.24. Verbatim Tags

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !<tag:yaml.org,2002:str> "foo"
          : !<!bar> "baz",
        }

    """

    text = dedent("""
        !<tag:yaml.org,2002:str> foo :
          !<!bar> baz

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_25__invalid_verbatim_tags():
    """
    Example 6.25. Invalid Verbatim Tags

    Expected:
        ERROR:
        - Verbatim tags aren't resolved,
          so ! is invalid.
        - The $:? tag is neither a global
          URI tag nor a local tag starting
          with  ! .

    """

    text = dedent("""
        - !<!> foo
        - !<$:?> bar

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


@feature_not_supported
def test_example_6_26__tag_shorthands():
    """
    Example 6.26. Tag Shorthands

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !<!local> "foo",
          !<tag:yaml.org,2002:str> "bar",
          !<tag:example.com,2000:app/tag!> "baz"
        ]

    """

    text = dedent("""
        %TAG !e! tag:example.com,2000:app/
        ---
        - !local foo
        - !!str bar
        - !e!tag%21 baz

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_27__invalid_tag_shorthands():
    """
    Example 6.27. Invalid Tag Shorthands

    Expected:
        ERROR:
        - The !o! handle has no suffix.
        - The !h! handle wasn't declared.

    """

    text = dedent("""
        %TAG !e! tag:example,2000:app/
        ---
        - !e! foo
        - !h!bar baz

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


@feature_not_supported
def test_example_6_28__non_specific_tags():
    """
    Example 6.28. Non-Specific Tags

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !<tag:yaml.org,2002:str> "12",
          !<tag:yaml.org,2002:int> "12",
          !<tag:yaml.org,2002:str> "12",
        ]

    """

    text = dedent("""
        # Assuming conventional resolution:
        - "12"
        - 12
        - ! 12

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Str('12'),
                    Int(12),
                    Str(12),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_6_29__node_anchors():
    """
    Example 6.29. Node Anchors

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "First occurrence"
          : &A !!str "Value",
          ? !!str "Second occurrence"
          : *A,
        }

    """

    text = dedent("""
        First occurrence: &anchor Value
        Second occurrence: *anchor

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (Str('First occurrence'), Str('Value')),
                    (Str('Second occurrence'), Str('Value')),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_7_1__alias_nodes():
    """
    Example 7.1. Alias Nodes

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "First occurrence"
          : &A !!str "Foo",
          ? !!str "Override anchor"
          : &B !!str "Bar",
          ? !!str "Second occurrence"
          : *A,
          ? !!str "Reuse anchor"
          : *B,
        }

    """

    text = dedent("""
        First occurrence: &anchor Foo
        Second occurrence: *anchor
        Override anchor: &anchor Bar
        Reuse anchor: *anchor

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (Str('First occurrence'), Str('Foo')),
                    (Str('Second occurrence'), Str('Foo')),
                    (Str('Override anchor'), Str('Bar')),
                    (Str('Reuse anchor'), Str('Bar')),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_7_2__empty_content():
    """
    Example 7.2. Empty Content

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "foo" : !!str "",
          ? !!str ""    : !!str "bar",
        }

    """

    text = dedent("""
        {
          foo : !!str ,
          !!str  : bar,
        }

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_7_3__completely_empty_flow_nodes():
    """
    Example 7.3. Completely Empty Flow Nodes

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "foo" : !!null "",
          ? !!null ""   : !!str "bar",
        }

    """

    text = dedent("""
        {
          ? foo : ,
           : bar,
        }

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_4__double_quoted_implicit_keys():
    """
    Example 7.4. Double Quoted Implicit Keys

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "implicit block key"
          : !!seq [
            !!map {
              ? !!str "implicit flow key"
              : !!str "value",
            }
          ]
        }

    """

    text = dedent("""
        "implicit block key" : [
          "implicit flow key" : value,
         ]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (
                        Str('implicit block key'),
                        Sequence(
                            Map(
                                (Str('implicit flow key'), Str('value'))
                            )
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_5__double_quoted_line_breaks():
    """
    Example 7.5. Double Quoted Line Breaks

    Expected:
        %YAML 1.2
        ---
        !!str "folded to a space,\n\
              to a line feed, \
              or \t \tnon-content"

    """

    text = dedent("""
        "folded
        to a space,

        to a line feed, or \t
         \t non-content"

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('folded  \nto a space,   to a line feed, or  \t \t  non-content'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_6__double_quoted_lines():
    """
    Example 7.6. Double Quoted Lines

    Expected:
        %YAML 1.2
        ---
        !!str " 1st non-empty\n\
              2nd non-empty \
              3rd non-empty "

    """

    text = dedent("""
        " 1st non-empty

         2nd non-empty
         3rd non-empty "

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str(' 1st non-empty\n2nd non-empty 3rd non-empty '),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_7__single_quoted_characters():
    """
    Example 7.7. Single Quoted Characters

    Expected:
        %YAML 1.2
        ---
        !!str "here's to \"quotes\""

    """

    text = dedent("""
         'here''s to "quotes"'
    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('here\'s to "quotes"'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_8__single_quoted_implicit_keys():
    """
    Example 7.8. Single Quoted Implicit Keys

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "implicit block key"
          : !!seq [
            !!map {
              ? !!str "implicit flow key"
              : !!str "value",
            }
          ]
        }

    """

    text = dedent("""
        'implicit block key' : [
          'implicit flow key' : value,
         ]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (
                        Str('implicit block key'),
                        Sequence(
                            Map(
                                (Str('implicit flow key'), Str('value'))
                            ),
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_9__single_quoted_lines():
    """
    Example 7.9. Single Quoted Lines

    Expected:
        %YAML 1.2
        ---
        !!str " 1st non-empty\n\
              2nd non-empty \
              3rd non-empty "

    """

    text = dedent("""
        ' 1st non-empty

         2nd non-empty
         3rd non-empty '

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str(' 1st non-empty\n2nd non-empty 3rd non-empty '),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_10__plain_characters():
    """
    Example 7.10. Plain Characters

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!str "::vector",
          !!str ": - ()",
          !!str "Up, up, and away!",
          !!int "-123",
          !!str "http://example.com/foo#bar",
          !!seq [
            !!str "::vector",
            !!str ": - ()",
            !!str "Up, up, and away!",
            !!int "-123",
            !!str "http://example.com/foo#bar",
          ],
        ]

    """

    text = dedent("""
        # Outside flow collection:
        - ::vector
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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_11__plain_implicit_keys():
    """
    Example 7.11. Plain Implicit Keys

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "implicit block key"
          : !!seq [
            !!map {
              ? !!str "implicit flow key"
              : !!str "value",
            }
          ]
        }

    """

    text = dedent("""
        implicit block key : [
          implicit flow key : value,
         ]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (
                        Str('implicit block key'),
                        Sequence(
                            Str('implicit flow key : value'),
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_12__plain_lines():
    """
    Example 7.12. Plain Lines

    Expected:
        %YAML 1.2
        ---
        !!str "1st non-empty\n\
              2nd non-empty \
              3rd non-empty"

    """

    text = dedent("""
        1st non-empty

         2nd non-empty
         3rd non-empty

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('1st non-empty\n2nd non-empty 3rd non-empty'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_13__flow_sequence():
    """
    Example 7.13. Flow Sequence

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!seq [
            !!str "one",
            !!str "two",
          ],
          !!seq [
            !!str "three",
            !!str "four",
          ],
        ]

    """

    text = dedent("""
        - [ one, two, ]
        - [three ,four]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Sequence(
                        Str('one'),
                        Str('two'),
                    ),
                    Sequence(
                        Str('three'),
                        Str('four'),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_14__flow_sequence_entries():
    """
    Example 7.14. Flow Sequence Entries

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!str "double quoted",
          !!str "single quoted",
          !!str "plain text",
          !!seq [
            !!str "nested",
          ],
          !!map {
            ? !!str "single"
            : !!str "pair",
          },
        ]

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_15__flow_mappings():
    """
    Example 7.15. Flow Mappings

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!map {
            ? !!str "one"   : !!str "two",
            ? !!str "three" : !!str "four",
          },
          !!map {
            ? !!str "five"  : !!str "six",
            ? !!str "seven" : !!str "eight",
          },
        ]

    """

    text = dedent("""
        - { one : two , three: four , }
        - {five: six,seven : eight}

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_7_16__flow_mapping_entries():
    """
    Example 7.16. Flow Mapping Entries

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "explicit" : !!str "entry",
          ? !!str "implicit" : !!str "entry",
          ? !!null "" : !!null "",
        }

    """

    text = dedent("""
        {
        ? explicit: entry,
        implicit: entry,
        ?
        }

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_17__flow_mapping_separate_values():
    """
    Example 7.17. Flow Mapping Separate Values

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "unquoted" : !!str "separate",
          ? !!str "http://foo.com" : !!null "",
          ? !!str "omitted value" : !!null "",
          ? !!null "" : !!str "omitted key",
        }

    """

    text = dedent("""
        {
        unquoted : "separate",
        http://foo.com,
        omitted value: ,
         : omitted key,
        }

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_18__flow_mapping_adjacent_values():
    """
    Example 7.18. Flow Mapping Adjacent Values

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "adjacent" : !!str "value",
          ? !!str "readable" : !!str "value",
          ? !!str "empty"    : !!null "",
        }

    """

    text = dedent("""
        {
        "adjacent":value,
        "readable": value,
        "empty":
        }

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (Str('"adjacent"'), Str('value')),
                    (Str('"readable"'), Str('value')),
                    (Str('"empty"'), Null(None)),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_19__single_pair_flow_mappings():
    """
    Example 7.19. Single Pair Flow Mappings

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!map { ? !!str "foo" : !!str "bar" }
        ]

    """

    text = dedent("""
        [
        foo: bar
        ]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Map(
                        (Str('foo'), Str('bar'))
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_7_20__single_pair_explicit_entry():
    """
    Example 7.20. Single Pair Explicit Entry

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!map {
            ? !!str "foo bar"
            : !!str "baz",
          },
        ]

    """

    text = dedent("""
        [
        ? foo
         bar : baz
        ]

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_21__single_pair_implicit_entries():
    """
    Example 7.21. Single Pair Implicit Entries

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!seq [
            !!map {
              ? !!str "YAML"
              : !!str "separate"
            },
          ],
          !!seq [
            !!map {
              ? !!null ""
              : !!str "empty key entry"
            },
          ],
          !!seq [
            !!map {
              ? !!map {
                ? !!str "JSON"
                : !!str "like"
              } : "adjacent",
            },
          ],
        ]

    """

    text = dedent("""
        - [ YAML : separate ]
        - [  : empty key entry ]
        - [ {JSON: like}:adjacent ]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Sequence(
                        Map(
                            (Str('YAML'), Str('separate')),
                        ),
                    ),
                    Sequence(
                        Map(
                            (Null(None), Str('empty key entry')),
                        ),
                    ),
                    Sequence(
                        Map(
                            (
                                Map(
                                    (Str('JSON'), Str('adjacent'))
                                ),
                                Str('adjacent')
                            ),
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_7_22__invalid_implicit_keys():
    """
    Example 7.22. Invalid Implicit Keys

    Expected:
        ERROR:
        - The foo bar key spans multiple lines
        - The foo...bar key is too long

    """

    text = dedent("""
        [ foo
         bar: invalid,
         "foo{long_key}bar": invalid ]

    """)[1:-1].format(long_key='abcdefghijklmnopqrstuvwxyz' * (1000 // 26))
    print(text)
    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


def test_example_7_23__flow_content():
    """
    Example 7.23. Flow Content

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!seq [ !!str "a", !!str "b" ],
          !!map { ? !!str "a" : !!str "b" },
          !!str "a",
          !!str "b",
          !!str "c",
        ]

    """

    text = dedent("""
        - [ a, b ]
        - { a: b }
        - "a"
        - 'b'
        - c

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Sequence(
                        Str('a'),
                        Str('b'),
                    ),
                    Map(
                        (Str('a'), Str('b')),
                    ),
                    Str('a'),
                    Str('b'),
                    Str('c'),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_7_24__flow_nodes():
    """
    Example 7.24. Flow Nodes

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!str "a",
          !!str "b",
          &A !!str "c",
          *A,
          !!str "",
        ]

    """

    text = dedent("""
        - !!str "a"
        - 'b'
        - &anchor "c"
        - *anchor
        - !!str

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_1__block_scalar_header():
    """
    Example 8.1. Block Scalar Header

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!str "literal\n",
          !!str " folded\n",
          !!str "keep\n\n",
          !!str " strip",
        ]

    """

    text = dedent("""
        - | # Empty header
         literal
        - >1 # Indentation indicator
          folded
        - |+ # Chomping indicator
         keep

        - >1- # Both indicators
          strip


    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_2__block_indentation_indicator():
    """
    Example 8.2. Block Indentation Indicator

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!str "detected\n",
          !!str "\n\n# detected\n",
          !!str " explicit\n",
          !!str "\t detected\n",
        ]

    """

    text = dedent("""
        - |
         detected
        - >


          # detected
        - |1
          explicit
        - >
         \t
         detected

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Sequence(
                    Str('detected\n'),
                    Str('\n\n# detected\n'),
                    Str('|1'),
                ),
            ),
            Doc(
                Str('explicit'),
            ),
            Doc(
                Sequence(
                    Str('\t detected\n'),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_3__invalid_block_scalar_indentation_indicators():
    """
    Example 8.3. Invalid Block Scalar Indentation Indicators

    Expected:
        ERROR:
        - A leading all-space line must
          not have too many spaces.
        - A following text line must
          not be less indented.
        - The text is less indented
          than the indicated level.

    """

    text = dedent("""
        - |

         text
        - >
          text
         text
        - |2
         text

    """)[1:-1]

    with raises(YAMLSyntaxError):
        nodes = parser.parse(text)
        print_nodes(nodes)


@feature_not_supported
def test_example_8_4__chomping_final_line_break():
    """
    Example 8.4. Chomping Final Line Break

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "strip"
          : !!str "text",
          ? !!str "clip"
          : !!str "text\n",
          ? !!str "keep"
          : !!str "text\n",
        }

    """

    text = dedent("""
        strip: |-
          text
        clip: |
          text
        keep: |+
          text

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_5__chomping_trailing_lines():
    """
    Example 8.5. Chomping Trailing Lines

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "strip"
          : !!str "# text",
          ? !!str "clip"
          : !!str "# text\n",
          ? !!str "keep"
          : !!str "# text\n",
        }

    """

    text = dedent("""
         # Strip
          # Comments:
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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected

@feature_not_supported
def test_example_8_6__empty_scalar_chomping():
    """
    Example 8.6. Empty Scalar Chomping

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "strip"
          : !!str "",
          ? !!str "clip"
          : !!str "",
          ? !!str "keep"
          : !!str "\n",
        }

    """

    text = dedent("""
        strip: >-

        clip: >

        keep: |+


    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (Str('strip'), Str('')),
                    (Str('clip'), Str('')),
                    (Str('keep'), Str('\n')),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_7__literal_scalar():
    """
    Example 8.7. Literal Scalar

    Expected:
        %YAML 1.2
        ---
        !!str "literal\n\ttext\n"

    """

    text = dedent("""
        |
         literal
         \ttext


    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('literal\n\ttext\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_8__literal_content():
    """
    Example 8.8. Literal Content

    Expected:
        %YAML 1.2
        ---
        !!str "\n\nliteral\n \n\ntext\n"

    """

    text = dedent("""
        |

          
          literal


          text

         # Comment

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('\n\nliteral\n text \n\n# Comment\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_9__folded_scalar():
    """
    Example 8.9. Folded Scalar

    Expected:
        %YAML 1.2
        ---
        !!str "folded text\n"

    """

    text = dedent("""
        >
         folded
         text


    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('folded  text\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_10__folded_lines():
    """
    Example 8.10. Folded Lines

    Expected:
        %YAML 1.2
        ---
        !!str "\n\
              folded line\n\
              next line\n\
              \  * bullet\n
              \n\
              \  * list\n\
              \  * lines\n\
              \n\
              last line\n"

    """

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

    expected = Docs(  # :off
            Doc(
                Str(' folded  line \nnext line    * bullet\n  * list   * lines\nlast  line\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_11__more_indented_lines():
    """
    Example 8.11. More Indented Lines

    Expected:
        %YAML 1.2
        ---
        !!str "\n\
              folded line\n\
              next line\n\
              \  * bullet\n
              \n\
              \  * list\n\
              \  * lines\n\
              \n\
              last line\n"

    """

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

    expected = Docs(  # :off
            Doc(
                Str(' folded line\nnext line   * bullet \n  * list    * lines \nlast line\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_12__empty_separation_lines():
    """
    Example 8.12. Empty Separation Lines

    Expected:
        %YAML 1.2
        ---
        !!str "\n\
              folded line\n\
              next line\n\
              \  * bullet\n
              \n\
              \  * list\n\
              \  * lines\n\
              \n\
              last line\n"

    """

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

    expected = Docs(  # :off
            Doc(
                Str(' folded line \nnext line    * bullet\n  * list   * line \nlast line\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_13__final_empty_lines():
    """
    Example 8.13. Final Empty Lines

    Expected:
        %YAML 1.2
        ---
        !!str "\n\
              folded line\n\
              next line\n\
              \  * bullet\n
              \n\
              \  * list\n\
              \  * lines\n\
              \n\
              last line\n"

    """

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

    expected = Docs(  # :off
            Doc(
                Str('folded line\nnext line   * bullet\n  * list   * line\nlast line\n'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_14__block_sequence():
    """
    Example 8.14. Block Sequence

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "block sequence"
          : !!seq [
            !!str "one",
            !!map {
              ? !!str "two"
              : !!str "three"
            },
          ],
        }

    """

    text = dedent("""
        block sequence:
          - one
          - two : three

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (
                        Str('block sequence'),
                        Sequence(
                            Str('one'),
                            Map(
                                (Str('two'), Str('three')),
                            ),
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_15__block_sequence_entry_types():
    """
    Example 8.15. Block Sequence Entry Types

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!null "",
          !!str "block node\n",
          !!seq [
            !!str "one"
            !!str "two",
          ],
          !!map {
            ? !!str "one"
            : !!str "two",
          },
        ]

    """

    text = dedent("""
        -  # Empty
        - |
         block node
        - - one # Compact
          - two # sequence
        - one: two # Compact mapping

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_8_16__block_mappings():
    """
    Example 8.16. Block Mappings

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "block mapping"
          : !!map {
            ? !!str "key"
            : !!str "value",
          },
        }

    """

    text = dedent("""
        block mapping:
         key: value

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (
                        Str('block mapping'),
                        Map(
                            (Str('key'), Str('value')),
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_17__explicit_block_mapping_entries():
    """
    Example 8.17. Explicit Block Mapping Entries

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "explicit key"
          : !!str "",
          ? !!str "block key\n"
          : !!seq [
            !!str "one",
            !!str "two",
          ],
        }

    """

    text = dedent("""
        ? explicit key # Empty value
        ? |
          block key
        : - one # Explicit compact
          - two # block value

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_18__implicit_block_mapping_entries():
    """
    Example 8.18. Implicit Block Mapping Entries

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "plain key"
          : !!str "in-line value",
          ? !!null ""
          : !!null "",
          ? !!str "quoted key"
          : !!seq [ !!str "entry" ],
        }

    """

    text = dedent("""
        plain key: in-line value
         :  # Both empty
        "quoted key":
        - entry

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_19__compact_block_mappings():
    """
    Example 8.19. Compact Block Mappings

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!map {
             !!str "sun" : !!str "yellow",
          },
          !!map {
            ? !!map {
              ? !!str "earth"
              : !!str "blue"
            },
            : !!map {
              ? !!str "moon"
              : !!str "white"
            },
          }
        ]

    """

    text = dedent("""
        - sun: yellow
        - ? earth: blue
          : moon: white

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_20__block_node_types():
    """
    Example 8.20. Block Node Types

    Expected:
        %YAML 1.2
        ---
        !!seq [
          !!str "flow in block",
          !!str "Block scalar\n",
          !!map {
            ? !!str "foo"
            : !!str "bar",
          },
        ]

    """

    text = dedent("""
        -
          "flow in block"
        - >
         Block scalar
        - !!map # Block collection
          foo : bar

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_21__block_scalar_nodes():
    """
    Example 8.21. Block Scalar Nodes

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "literal"
          : !!str "value",
          ? !!str "folded"
          : !<!foo> "value",
        }

    """

    text = dedent("""
        literal: |2
          value
        folded:
           !foo
          >1
         value

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_8_22__block_collection_nodes():
    """
    Example 8.22. Block Collection Nodes

    Expected:
        %YAML 1.2
        ---
        !!map {
          ? !!str "sequence"
          : !!seq [
            !!str "entry",
            !!seq [ !!str "nested" ],
          ],
          ? !!str "mapping"
          : !!map {
            ? !!str "foo" : !!str "bar",
          },
        }

    """

    text = dedent("""
        sequence: !!seq
        - entry
        - !!seq
         - nested
        mapping: !!map
         foo: bar

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_9_1__document_prefix():
    """
    Example 9.1. Document Prefix

    Expected:
        %YAML 1.2
        ---
        !!str "Document"

    """

    text = dedent("""
         # Comment
        # lines
        Document

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('Document'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_9_2__document_markers():
    """
    Example 9.2. Document Markers

    Expected:
        %YAML 1.2
        ---
        !!str "Document"

    """

    text = dedent("""
        %YAML 1.2
        ---
        Document
        ... # Suffix

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Str('%YAML 1.2'),
            ),
            Doc(
                Str('Document'),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_9_3__bare_documents():
    """
    Example 9.3. Bare Documents

    Expected:
        %YAML 1.2
        ---
        !!str "Bare document"
        %YAML 1.2
        ---
        !!str "%!PS-Adobe-2.0\n"

    """

    text = dedent("""
        Bare
        document
        ...
        # No document
        ...
        |
        %!PS-Adobe-2.0 # Not the first line

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_9_4__explicit_documents():
    """
    Example 9.4. Explicit Documents

    Expected:
        %YAML 1.2
        ---
        !!map {
          !!str "matches %": !!int "20"
        }
        ...
        %YAML 1.2
        ---
        !!null ""

    """

    text = dedent("""
        ---
        { matches
        % : 20 }
        ...
        ---
        # Empty
        ...

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_9_5__directives_documents():
    """
    Example 9.5. Directives Documents

    Expected:
        %YAML 1.2
        ---
        !!str "%!PS-Adobe-2.0\n"
        ...
        %YAML 1.2
        ---
        !!null ""

    """

    text = dedent("""
        %YAML 1.2
        --- |
        %!PS-Adobe-2.0
        ...
        %YAML1.2
        ---
        # Empty
        ...

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_9_6__stream():
    """
    Example 9.6. Stream

    Expected:
        %YAML 1.2
        ---
        !!str "Document"
        ...
        %YAML 1.2
        ---
        !!null ""
        ...
        %YAML 1.2
        ---
        !!map {
          !!str "matches %": !!int "20"
        }

    """

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

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


def test_example_10_8__json_tag_resolution():
    """
    Example 10.8. JSON Tag Resolution

    Expected:
        %YAML 1.2
        ---
        !!map {
          !!str "A null" : !!null "null",
          !!str "Booleans: !!seq [
            !!bool "true", !!bool "false"
          ],
          !!str "Integers": !!seq [
            !!int "0", !!int "-0",
            !!int "3", !!int "-19"
          ],
          !!str "Floats": !!seq [
            !!float "0.", !!float "-0.0",
            !!float "12e03", !!float "-2E+05"
          ],
          !!str "Invalid": !!seq [
            # Rejected by the schema
            True, Null, 0o7, 0x3A, +12.3,
          ],
        }
        ...

    """

    text = dedent("""
        A null: null
        Booleans: [ true, false ]
        Integers: [ 0, -0, 3, -19 ]
        Floats: [ 0., -0.0, 12e03, -2E+05 ]
        Invalid: [ True, Null, 0o7, 0x3A, +12.3 ]

    """)[1:-1]

    expected = Docs(  # :off
            Doc(
                Map(
                    (Str('A null'), Null(None)),
                    (
                        Str('Booleans'),
                        Sequence(
                            Bool(True),
                        ),
                    ),
                    (
                        Str('Integers'),
                        Sequence(
                            Int(3),
                            Int(-19),
                        ),
                    ),
                    (
                        Str('Floats'),
                        Sequence(
                            Float(12000.0),
                            Float(-200000.0),
                        ),
                    ),
                    (
                        Str('Invalid'),
                        Sequence(
                            Bool(True),
                            Int(7),
                            Int(58),
                            Float(12.3),
                        ),
                    ),
                ),
            ),
        )  # :on

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected


@feature_not_supported
def test_example_10_9__core_tag_resolution():
    """
    Example 10.9. Core Tag Resolution

    Expected:
        %YAML 1.2
        ---
        !!map {
          !!str "A null" : !!null "null",
          !!str "Also a null" : !!null "",
          !!str "Not a null" : !!str "",
          !!str "Booleans: !!seq [
            !!bool "true", !!bool "True",
            !!bool "false", !!bool "FALSE",
          ],
          !!str "Integers": !!seq [
            !!int "0", !!int "0o7",
            !!int "0x3A", !!int "-19",
          ],
          !!str "Floats": !!seq [
            !!float "0.", !!float "-0.0", !!float ".5",
            !!float "+12e03", !!float "-2E+05"
          ],
          !!str "Also floats": !!seq [
            !!float ".inf", !!float "-.Inf",
            !!float "+.INF", !!float ".NAN",
          ],
        }
        ...

    """

    text = dedent("""
        A null: null
        Also a null: # Empty
        Not a null: ""
        Booleans: [ true, True, false, FALSE ]
        Integers: [ 0, 0o7, 0x3A, -19 ]
        Floats: [ 0., -0.0, .5, +12e03, -2E+05 ]
        Also floats: [ .inf, -.Inf, +.INF, .NAN ]

    """)[1:-1]

    expected = None

    nodes = parser.parse(text)
    print_nodes(nodes)

    assert nodes == expected
