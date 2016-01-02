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
    expected = Docs(Doc(String('Hello World')))

    assert nodes == expected


def test_doc_with_no_end_of_doc_indicator():
    text = dedent("""
        ---
        Hello World
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(String('Hello World')))

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
    expected = Docs(Doc(String('Hello World')), Doc(String('Foo Bar')))

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
        Doc(String('Hello World')),
        Doc(String('Foo Bar')),
        Doc(String('More Docs'))
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
        Doc(String('Hello World')),
        Doc(String('Foo Bar')),
        Doc(String('More Docs'))
    )  # :on

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
    expected = Docs(Doc(Sequence(String('Hello World', ))))

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
        String('Hello World'),
        String('Foo Bar'),
    )))  # :on

    print(nodes)
    assert nodes == expected


def test_three_item_sequence():
    text = dedent("""
        ---
        - Hello World
        - Foo Bar
        - More Items
        ...
    """)[1:-1]

    nodes = parser.parse(text)
    expected = Docs(Doc(Sequence(  # :off
        String('Hello World'),
        String('Foo Bar'),
        String('More Items'),
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
        (String('Hello'), String('World'))
    )))  # :on

    assert nodes == expected
