# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from ply.lex import lex
from ply.yacc import yacc

from .nodes import *

tokens = ['DOC_START_INDICATOR', 'DOC_END_INDICATOR', 'STRING', 'INT']

t_DOC_START_INDICATOR = r'---'
t_DOC_END_INDICATOR = r'\.\.\.'
# t_SEQUENCE_INDICATOR = r'- '
t_ignore_EOL = r'\s*\n'
t_STRING = r'[\w ]+'
t_INT = r'[\d]+'


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
    """
    p[0] = Doc(p[1])


def p_scalar_string(p):
    """
    scalar  : STRING
    """
    p[0] = String(p[1])


def p_error(p):
    print('Syntax error')


parser = yacc(debug=True)
