# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from ply.lex import lex
from ply.yacc import yacc

from .nodes import *  # noqa


def find_column(token):
    text = token.lexer.lexdata
    last_cr = text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


# LEXER
# ===================================================================
tokens = [  # :off
    'DOC_START_INDICATOR',
    'DOC_END_INDICATOR',
    'SEQUENCE_INDICATOR',
    'MAP_INDICATOR',
    'CAST_TYPE',
    'FLOAT',
    'INT',
    'BOOL',
    'STRING',
    'LITERAL_LINE',
    'INDENT',
    'DEDENT',
    'NODENT',
]  # :on

states = (  # :off
    ('tag', 'inclusive'),
    ('doublequote', 'exclusive'),
    ('comment', 'exclusive'),
    ('singlequote', 'exclusive'),
    ('literal', 'exclusive'),

)  # :on


# state: multiple
# -------------------------------------------------------------------
def setup_indent(t):
    # strip newline
    t.value = t.value[1:]

    # initialize
    is_first_indent_found = any([  # :off
        not hasattr(t.lexer, 'indent_token_size'),
        not t.lexer.indent_token_size
    ])  # :on
    if is_first_indent_found:
        t.lexer.indent_token_size = len(t.value)
    if not hasattr(t.lexer, 'indent_depth'):
        t.lexer.indent_depth = 0

    # calculate depth
    indent_token_size = t.lexer.indent_token_size
    if indent_token_size > 0:
        indent_depth = len(t.value) // indent_token_size
    else:
        indent_depth = 0

    # calculate change in depth
    indent_delta = indent_depth - t.lexer.indent_depth

    # set current indent_depth and indent_delta
    t.lexer.indent_delta, t.lexer.indent_depth = indent_delta, indent_depth

    return t


def t_ignore_INDENT(t):
    r'\n\ +'

    t = setup_indent(t)

    indent_delta = t.lexer.indent_delta

    if indent_delta > 0:
        t.type = 'INDENT'
    elif indent_delta < 0:
        t.type = 'DEDENT'
    else:
        t.type = 'NODENT'

    return t


def t_ANY_error(t):
    raise SyntaxError('Bad character: {!r}'.format(t.value[0]))


# state: tag
# -------------------------------------------------------------------
def t_begin_tag(t):
    r'(?<!\\)!'
    t.lexer.push_state('tag')


def t_tag_end(t):
    r'\ '
    t.lexer.pop_state()


def t_tag_CAST_TYPE(t):
    r'(?<=\!)[a-z]+'
    return t


# state: doublequote
# -------------------------------------------------------------------

t_doublequote_STRING = r'(?:\\"|[^"])+'


def t_begin_doublequote(t):
    r'(?<!\\)"'
    t.lexer.begin('doublequote')


def t_doublequote_end(t):
    r'(?<!\\)"'
    t.lexer.begin('INITIAL')


# state: comment
# -------------------------------------------------------------------
def t_begin_comment(t):
    r'\s*\# '
    t.lexer.begin('comment')


def t_comment_end(t):
    r'\n'
    t.lexer.begin('INITIAL')


def t_comment_ignore_COMMENT(t):
    r'[^\n]+'


# state: singlequote
# -------------------------------------------------------------------

t_singlequote_STRING = r"(?:\\'|[^'])+"


def t_begin_singlequote(t):
    r"(?<!\\)'"
    t.lexer.begin('singlequote')


def t_singlequote_end(t):
    r"(?<!\\)'"
    t.lexer.begin('INITIAL')


# state: literal
# -------------------------------------------------------------------

def t_literal_LITERAL_LINE(t):
    r'[\w\s]+'
    return t


def t_begin_literal(t):
    r'(?<!\\)\|'
    t.lexer.begin('literal')


def t_literal_end(t):
    r'\n\n'
    t.lexer.begin('INITIAL')


# def t_literal_UNDENT(t):
#     pass


# state: INITIAL
# -------------------------------------------------------------------

t_DOC_START_INDICATOR = r'---'
t_DOC_END_INDICATOR = r'\.\.\.'
t_SEQUENCE_INDICATOR = r'-\ '
t_MAP_INDICATOR = r':\ *'
t_ignore_EOL = r'\s*\n'


def t_FLOAT(t):
    r'\d*\.\d+'
    return t


def t_INT(t):
    r'\d+'
    return t


def t_BOOL(t):
    r'Yes|No'
    return t


def t_STRING(t):
    r'(?:\\.)|[\w ,!\\]+'
    return t


lexer = lex(debug=True)


# PARSER
# ===================================================================
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


def p_docs_implicit(p):
    """
    docs    : doc
    """
    p[0] = p[1]


def p_doc(p):
    """
    doc : collection
        | scalar
    """
    p[0] = Doc(p[1])


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


def p_scalar_explicit_cast(p):
    """
    scalar  : CAST_TYPE scalar
    """
    type_nodes = {'int': Int, 'str': Str, 'float': Float}
    p[0] = type_nodes[p[1]](p[2].value)


def p_scalar_float(p):
    """
    scalar  : FLOAT
    """

    p[0] = Float(p[1])


def p_scalar_int(p):
    """
    scalar  : INT
    """

    p[0] = Int(p[1])


def p_scalar_bool(p):
    """
    scalar  : BOOL
    """
    p[0] = Bool(p[1])


def p_scalar_literal(p):
    """
    scalar  : literal_lines
    """
    p[0] = p[1]


def p_scalar_string(p):
    """
    scalar  : STRING
    """
    p[0] = Str(p[1])


def p_literal_lines(p):
    """
    literal_lines   : LITERAL_LINE
    """
    p[0] = p[1]


def p_error(p):
    raise SyntaxError('Unexpected expression: {0!r}:{1!r}'.format(p.type, p.value))


parser = yacc(debug=True)
