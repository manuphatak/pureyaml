# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from ply.lex import lex
from ply.yacc import yacc

from .nodes import *

tokens = [  # :off
    'DOC_START_INDICATOR',
    'DOC_END_INDICATOR',
    'SEQUENCE_INDICATOR',
    'MAP_INDICATOR',
    'INT',
    'STRING',
]  # :on

t_DOC_START_INDICATOR = r'---'
t_DOC_END_INDICATOR = r'\.\.\.'
t_SEQUENCE_INDICATOR = r'-\ '
t_MAP_INDICATOR = r':\ *'
t_ignore_EOL = r'\s*\n'


def t_INT(t):
    r'[\d]+'
    return t


def t_STRING(t):
    r'[\w ]+'
    return t


def t_error(t):
    raise SyntaxError('Bad character: {!r}'.format(t.value[0]))


lexer = lex(debug=True)


def p_docs_init(p):
    """
    docs    : DOC_START_INDICATOR doc DOC_END_INDICATOR docs
            | DOC_START_INDICATOR doc docs
    """
    if len(p) == 5:
        docs = p[4]
    else:
        docs = p[3]

    p[0] = Docs(p[2]) + docs


def p_docs_last(p):
    """
    docs    : DOC_START_INDICATOR doc DOC_END_INDICATOR
            | DOC_START_INDICATOR doc
    """
    p[0] = Docs(p[2])


def p_doc(p):
    """
    doc : scalar
        | collection
    """
    p[0] = Doc(p[1])


def p_scalar_int(p):
    """
    scalar  : INT
    """

    p[0] = Int(p[1])


def p_scalar_string(p):
    """
    scalar  : STRING
    """
    p[0] = String(p[1])


def p_collection(p):
    """
    collection  : sequence
                | map
    """
    p[0] = p[1]


def p_map_init(p):
    """
    map : map_item map
    """
    p[0] = Map(p[1]) + p[2]


def p_map_last(p):
    """
    map : map_item
    """
    p[0] = Map(p[1])


def p_map_item(p):
    """
    map_item    : scalar MAP_INDICATOR scalar
    """
    p[0] = p[1], p[3]


def p_sequence_init(p):
    """
    sequence    : sequence_item sequence
    """
    p[0] = Sequence(p[1]) + p[2]


def p_sequence_last(p):
    """
    sequence    : sequence_item
    """
    p[0] = Sequence(p[1])


def p_sequence_item(p):
    """
    sequence_item   : SEQUENCE_INDICATOR scalar
    """
    p[0] = p[2]


def p_error(p):
    raise SyntaxError('Unexpected expression: {0!r}:{1!r}'.format(p.type, p.value))


parser = yacc(debug=True)
