#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from textwrap import dedent

from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import feature_not_supported

parser = YAMLParser(debug=True)


def parse(text):
    nodes = parser.parse(text)
    return nodes


def test_ex_2_01_sequence_of_scalars():
    text = dedent("""
        - Mark McGwire
        - Sammy Sosa
        - Ken Griffey
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Sequence(
                Str('Mark McGwire'),
                Str('Sammy Sosa'),
                Str('Ken Griffey'),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_02_mapping_scalars_to_scalars():
    text = dedent("""
        hr:  65    # Home runs
        avg: 0.278 # Batting average
        rbi: 147   # Runs Batted In
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('hr'), Int(65)),
                (Str('avg'), Float(0.278)),
                (Str('rbi'), Int(147)),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_03_mapping_scalars_to_sequences():
    text = dedent("""
        american:
          - Boston Red Sox
          - Detroit Tigers
          - New York Yankees
        national:
          - New York Mets
          - Chicago Cubs
          - Atlanta Braves
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('american'),
                    Sequence(
                        Str('Boston Red Sox'),
                        Str('Detroit Tigers'),
                        Str('New York Yankees'),
                    ),
                ),
                (
                    Str('national'),
                    Sequence(
                        Str('New York Mets'),
                        Str('Chicago Cubs'),
                        Str('Atlanta Braves'),
                    ),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_04_sequence_of_mappings():
    text = dedent("""
        -
          name: Mark McGwire
          hr:   65
          avg:  0.278
        -
          name: Sammy Sosa
          hr:   63
          avg:  0.288
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Sequence(
                Map(
                    (Str('name'), Str('Mark McGwire')),
                    (Str('hr'), Int(65)),
                    (Str('avg'), Float(0.278)),
                ),
                Map(
                    (Str('name'), Str('Sammy Sosa')),
                    (Str('hr'), Int(63)),
                    (Str('avg'), Float(0.288)),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_05_sequence_of_sequences():
    text = dedent("""
        - [name        , hr, avg  ]
        - [Mark McGwire, 65, 0.278]
        - [Sammy Sosa  , 63, 0.288]
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Sequence(
                Sequence(
                    Str('name'),
                    Str('hr'),
                    Str('avg'),
                ),
                Sequence(
                    Str('Mark McGwire'),
                    Int(65),
                    Float(0.278),
                ),
                Sequence(
                    Str('Sammy Sosa'),
                    Int(63),
                    Float(0.288),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_06_mapping_of_mappings():
    text = dedent("""
        Mark McGwire: {hr: 65, avg: 0.278}
        Sammy Sosa: {
            hr: 63,
            avg: 0.288
          }
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('Mark McGwire'),
                    Map(
                        (Str('hr'), Int(65)),
                        (Str('avg'), Float(0.278)),
                    ),
                ),
                (
                    Str('Sammy Sosa'),
                    Map(
                        (Str('hr'), Int(63)),
                        (Str('avg'), Float(0.288)),
                    ),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_07_two_docs_in_a_stream():
    text = dedent("""
        # Ranking of 1998 home runs
        ---
        - Mark McGwire
        - Sammy Sosa
        - Ken Griffey

        # Team ranking
        ---
        - Chicago Cubs
        - St Louis Cardinals
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Sequence(
                Str('Mark McGwire'),
                Str('Sammy Sosa'),
                Str('Ken Griffey'),
            ),
        ),
        Doc(
            Sequence(
                Str('Chicago Cubs'),
                Str('St Louis Cardinals'),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_08_play_by_play_feed():
    text = dedent("""
        ---
        time: 20:03:20
        player: Sammy Sosa
        action: strike (miss)
        ...
        ---
        time: 20:03:47
        player: Sammy Sosa
        action: grand slam
        ...
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('time'), Str('20:03:20')),
                (Str('player'), Str('Sammy Sosa')),
                (Str('action'), Str('strike (miss)')),
            ),
        ),
        Doc(
            Map(
                (Str('time'), Str('20:03:47')),
                (Str('player'), Str('Sammy Sosa')),
                (Str('action'), Str('grand slam')),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_09_single_doc_with_two_comments():
    text = dedent("""
        ---
        hr: # 1998 hr ranking
          - Mark McGwire
          - Sammy Sosa
        rbi:
          # 1998 rbi ranking
          - Sammy Sosa
          - Ken Griffey
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('hr'),
                    Sequence(
                        Str('Mark McGwire'),
                        Str('Sammy Sosa'),
                    ),
                ),
                (
                    Str('rbi'),
                    Sequence(
                        Str('Sammy Sosa'),
                        Str('Ken Griffey'),
                    ),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


@feature_not_supported
def test_ex_2_10_node_appears_twice():
    text = dedent("""
        ---
        hr:
          - Mark McGwire
          # Following node labeled SS
          - &SS Sammy Sosa
        rbi:
          - *SS # Subsequent occurrence
          - Ken Griffey
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('hr'),
                    Sequence(
                        Str('Mark McGwire'),
                        Str('Sammy Sosa'),
                    ),
                ),
                (
                    Str('rbi'),
                    Sequence(
                        Str('Sammy Sosa'),
                        Str('Ken Griffey'),
                    ),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_11_mapping_between_sequences():
    text = dedent("""
        ? - Detroit Tigers
          - Chicago cubs
        :
          - 2001-07-23

        ? [ New York Yankees,
            Atlanta Braves ]
        : [ 2001-07-02, 2001-08-12,
            2001-08-14 ]
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Sequence(
                        Str('Detroit Tigers'),
                        Str('Chicago cubs'),
                    ),
                    Sequence(
                        Str('2001-07-23'),
                    ),
                ),
                (
                    Sequence(
                        Str('New York Yankees'),
                        Str('Atlanta Braves'),
                    ),
                    Sequence(
                        Str('2001-07-02'),
                        Str('2001-08-12'),
                        Str('2001-08-14'),
                    ),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_12_compat_nested_mapping():
    text = dedent("""
        ---
        # Products purchased
        - item    : Super Hoop
          quantity: 1
        - item    : Basketball
          quantity: 4
        - item    : Big Shoes
          quantity: 1
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Sequence(
                Map(
                    (Str('item'), Str('Super Hoop')),
                    (Str('quantity'), Int(1)),
                ),
                Map(
                    (Str('item'), Str('Basketball')),
                    (Str('quantity'), Int(4)),
                ),
                Map(
                    (Str('item'), Str('Big Shoes')),
                    (Str('quantity'), Int(1)),
                ),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_13_literal_newlines_are_preserved():
    text = dedent("""
        # ASCII Art
        --- |
          \//||\/||
          // ||  ||__
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Str('\\//||\\/||\n// ||  ||__\n'),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_14_folded_newlines_become_spaces():
    text = dedent("""
        --- >
          Mark McGwire's
          year was crippled
          by a knee injury.
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Str("Mark McGwire's year was crippled by a knee injury.\n"),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_15_folded_indents_and_blank_lines_preserved():
    text = dedent("""
        >
         Sammy Sosa completed another
         fine season with great stats.

           63 Home Runs
           0.288 Batting Average

         What a year!
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Str('Sammy Sosa completed another fine season with great stats.\n  63 Home Runs   0.288 Batting '
                'Average\nWhat a year!\n'),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_16_indentation_determines_scope():
    text = dedent("""
        name: Mark McGwire
        accomplishment: >
          Mark set a major league
          home run record in 1998.
        stats: |
          65 Home Runs
          0.278 Batting Average
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('name'), Str('Mark McGwire')),
                (Str('accomplishment'), Str('Mark set a major league home run record in 1998.\n')),
                (Str('stats'), Str('65 Home Runs\n0.278 Batting Average\n')),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_17_quoted_scalars():
    text = dedent(r"""
        unicode: "Sosa did fine.\u263A"
        control: "\b1998\t1999\t2000\n"
        hex esc: "\x0d\x0a is \r\n"

        single: '"Howdy!" he cried.'
        quoted: ' # Not a ''comment''.'
        tie-fighter: '|\-*-/|'
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('unicode'), Str(r'Sosa did fine.\u263A')),
                (Str('control'), Str(r'\b1998\t1999\t2000\n')),
                (Str('hex esc'), Str(r'\x0d\x0a is \r\n')),
                (Str('single'), Str('"Howdy!" he cried.')),
                (Str('quoted'), Str(" # Not a 'comment'.")),
                (Str('tie-fighter'), Str(r'|\-*-/|')),
            )
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_18_multi_line_flow_scalars():
    text = dedent("""
        plain:
          This unquoted scalar
          spans many lines.

        quoted: "So does this
          quoted scalar.\n"
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('This unquoted scalar spans many lines.')),
                (Str('quoted'), Str('So does this quoted scalar.\n')),
            )
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_19_integers():
    text = dedent("""
        canonical: 12345
        decimal: +12345
        octal: 0o14
        hexadecimal: 0xC
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('canonical'), Int(12345)),
                (Str('decimal'), Int(12345)),
                (Str('octal'), Int(12)),
                (Str('hexadecimal'), Int(12)),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_20_floating_point():
    text = dedent("""
        canonical: 1.23015e+3
        exponential: 12.3015e+02
        fixed: 1230.15
        negative infinity: -.inf
        not a number: .NaN
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('canonical'), Float(1230.15)),
                (Str('exponential'), Float(1230.15)),
                (Str('fixed'), Float(1230.15)),
                (Str('negative infinity'), Float('-inf')),
                (Str('not a number'), Float('nan')),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_21_miscellaneous():
    # TODO uncomment null
    text = dedent("""
        # null:
        booleans: [ true, false ]
        string: '012345'
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (
                    Str('booleans'),
                    Sequence(
                        Bool(True),
                        Bool(False),
                    ),
                ),
                (Str('string'), Str('012345')),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_22_timestamps():
    text = dedent("""
        canonical: 2001-12-15T02:59:43.1Z
        iso8601: 2001-12-14t21:59:43.10-05:00
        spaced: 2001-12-14 21:59:43.10 -5
        date: 2002-12-14
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('canonical'), Str('2001-12-15T02:59:43.1Z')),
                (Str('iso8601'), Str('2001-12-14t21:59:43.10-05:00')),
                (Str('spaced'), Str('2001-12-14 21:59:43.10 -5')),
                (Str('date'), Str('2002-12-14')),
            ),
        ),
    )  # :on

    assert parse(text) == expected


def test_ex_2_23_various_explicit_tags():
    # TODO, remove comments
    # noinspection SpellCheckingInspection
    text = dedent("""
        ---
        not-date: !!str 2002-04-28

        picture: !!binary |
         R0lGODlhDAAMAIQAAP//9/X
         17unp5WZmZgAAAOfn515eXv
         Pz7Y6OjuDg4J+fn5OTk6enp
         56enmleECcgggoBADs=

        # application specific tag: !something |
        #  The semantics of the tag
        #  above may be different for
        #  different documents.
    """)[1:]

    # noinspection SpellCheckingInspection
    expected = Docs(  # :off
        Doc(
            Map(
                (Str('not-date'), Str('2002-04-28')),
                (
                    Str('picture'),
                    Binary(dedent("""
                        R0lGODlhDAAMAIQAAP//9/X
                        17unp5WZmZgAAAOfn515eXv
                        Pz7Y6OjuDg4J+fn5OTk6enp
                        56enmleECcgggoBADs=
                    """)[1:-1])
                ),
            ),
        ),
    )  # :on
    assert parse(text) == expected


@feature_not_supported
def test_ex_2_24_global_tags():
    text = dedent("""
        %TAG ! tag:clarkevans.com,2002:
        --- !shape
          # Use the ! handle for presenting
          # tag:clarkevans.com,2002:circle
        - !circle
          center: &ORIGIN {x: 73, y: 129}
          radius: 7
        - !line
          start: *ORIGIN
          finish: { x: 89, y: 102 }
        - !label
          start: *ORIGIN
          color: 0xFFEEBB
          text: Pretty vector drawing.
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('This unquoted scalar spans many lines.')),
                (Str('quoted'), Str('So does this quoted scalar.\n')),
            )
        ),
    )  # :on

    assert parse(text) == expected


@feature_not_supported
def test_ex_2_25_unordered_sets():
    text = dedent("""
        # Sets are represented as a
        # Mapping where each key is
        # associated with a null value
        --- !!set
        ? Mark McGwire
        ? Sammy Sosa
        ? Ken Griff
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('This unquoted scalar spans many lines.')),
                (Str('quoted'), Str('So does this quoted scalar.\n')),
            )
        ),
    )  # :on

    assert parse(text) == expected


@feature_not_supported
def test_ex_2_26_ordered_mappings():
    text = dedent("""
        # Ordered maps are represented as
        # A sequence of mappings, with
        # each mapping having one key
        --- !!omap
        - Mark McGwire: 65
        - Sammy Sosa: 63
        - Ken Griffy: 58
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('This unquoted scalar spans many lines.')),
                (Str('quoted'), Str('So does this quoted scalar.\n')),
            )
        ),
    )  # :on

    assert parse(text) == expected


@feature_not_supported
def test_ex_2_27_invoice():
    text = dedent("""
        --- !<tag:clarkevans.com,2002:invoice>
        invoice: 34843
        date   : 2001-01-23
        bill-to: &id001
            given  : Chris
            family : Dumars
            address:
                lines: |
                    458 Walkman Dr.
                    Suite #292
                city    : Royal Oak
                state   : MI
                postal  : 48046
        ship-to: *id001
        product:
            - sku         : BL394D
              quantity    : 4
              description : Basketball
              price       : 450.00
            - sku         : BL4438H
              quantity    : 1
              description : Super Hoop
              price       : 2392.00
        tax  : 251.42
        total: 4443.52
        comments:
            Late afternoon is best.
            Backup contact is Nancy
            Billsmer @ 338-4338.
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('This unquoted scalar spans many lines.')),
                (Str('quoted'), Str('So does this quoted scalar.\n')),
            )
        ),
    )  # :on

    assert parse(text) == expected


@feature_not_supported
def test_ex_2_28_log_file():
    text = dedent("""
        ---
        Time: 2001-11-23 15:01:42 -5
        User: ed
        Warning:
          This is an error message
          for the log file
        ---
        Time: 2001-11-23 15:02:31 -5
        User: ed
        Warning:
          A slightly different error
          message.
        ---
        Date: 2001-11-23 15:03:17 -5
        User: ed
        Fatal:
          Unknown variable "bar"
        Stack:
          - file: TopClass.py
            line: 23
            code: |
              x = MoreObject("345\n")
          - file: MoreClass.py
            line: 58
            code: |-
              foo = bar
    """)[1:]

    expected = Docs(  # :off
        Doc(
            Map(
                (Str('plain'), Str('This unquoted scalar spans many lines.')),
                (Str('quoted'), Str('So does this quoted scalar.\n')),
            )
        ),
    )  # :on

    assert parse(text) == expected
