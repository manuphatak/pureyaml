# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from functools import wraps
from textwrap import dedent

from .exceptions import YAMLStrictTypeError
from .nodes import *  # noqa
from .utils import fold


class TokenList(object):
    tokens = [  # :off
        'DOC_START_INDICATOR',
        'DOC_END_INDICATOR',
        'SEQUENCE_INDICATOR',
        'MAP_INDICATOR',
        'LITERAL_INDICATOR_START',
        'LITERAL_INDICATOR_END',
        'FOLD_INDICATOR_START',
        'FOLD_INDICATOR_END',
        'CAST_TYPE',
        'SCALAR',
        'INDENT',
        'DEDENT',
    ]  # :on


def find_column(t):
    pos = t.lexpos + len(t.value)
    data = t.lexer.lexdata
    last_cr = data.rfind('\n', 0, pos)
    if last_cr < 0:
        last_cr = 0
    column = pos - last_cr
    return column


class YAMLTokens(TokenList):
    def __init__(self):
        self.indent_stack = [1]
        self.doc_context_stack = []

    # LEXER
    # ===================================================================
    states = (  # :off
        ('tag', 'inclusive'),
        ('doublequote', 'exclusive'),
        ('comment', 'exclusive'),
        ('singlequote', 'exclusive'),
        ('literal', 'exclusive'),
        ('fold', 'exclusive')

    )  # :on

    # state: multiple
    # -------------------------------------------------------------------
    def t_eof(self, t):
        if self.doc_context_stack:
            self.doc_context_stack.pop()
            t.type = 'DOC_END_INDICATOR'
            return t

    def t_ignore_INDENT(self, t):
        r'\n\s*(?=\S)|\n(?=$)'

        indent_stack = self.indent_stack
        column = find_column(t)
        assert indent_stack == sorted(indent_stack)
        next_indent_length, curr_indent_length = column, self.indent_stack[-1]
        if next_indent_length > curr_indent_length:
            indent_stack.append(next_indent_length)
            t.type = 'INDENT'
            return t

        elif next_indent_length == curr_indent_length:
            # NODENT
            pass
        else:
            indent_delta = curr_indent_length - indent_stack.pop()
            t.lexer.lexpos -= indent_delta

            t.type = 'DEDENT'
            return t

    # state: tag
    # -------------------------------------------------------------------
    def t_begin_tag(self, t):
        r'(?<!\\)!'
        t.lexer.push_state('tag')

    def t_tag_end(self, t):
        r'\ '
        t.lexer.pop_state()

    def t_tag_CAST_TYPE(self, t):
        r'(?<=\!)[a-z]+'
        return t

    # state: doublequote
    # -------------------------------------------------------------------
    t_doublequote_SCALAR = r'(?:\\"|[^"])+'

    def t_begin_doublequote(self, t):
        r'(?<!\\)"'

        t.lexer.push_state('doublequote')
        # t.lexer.begin('doublequote')
        t.type = 'CAST_TYPE'
        t.value = 'str'
        return t

    def t_doublequote_end(self, t):
        r'(?<!\\)"'
        t.lexer.pop_state()
        # t.lexer.begin('INITIAL')

    # state: comment
    # -------------------------------------------------------------------
    t_comment_ignore_COMMENT = r'[^\n]+'

    def t_begin_comment(self, t):
        r'\s*\#\ ?'
        t.lexer.push_state('comment')
        # t.lexer.begin('comment')

    def t_comment_end(self, t):
        r'(?=\n)'
        # t.lexer.begin('INITIAL')
        t.lexer.pop_state()

    # state: singlequote
    # -------------------------------------------------------------------
    t_singlequote_SCALAR = r"(?:\\'|[^'])+"

    def t_begin_singlequote(self, t):
        r"(?<!\\)'"
        t.lexer.push_state('singlequote')
        # t.lexer.begin('singlequote')
        t.type = 'CAST_TYPE'
        t.value = 'str'
        return t

    def t_singlequote_end(self, t):
        r"(?<!\\)'"
        # t.lexer.begin('INITIAL')
        t.lexer.pop_state()

    # state: literal
    # -------------------------------------------------------------------
    t_literal_SCALAR = r'.+'

    def t_begin_literal(self, t):
        r'\ *(?<!\\)\|\ ?\n'
        t.lexer.push_state('literal')
        t.type = 'LITERAL_INDICATOR_START'
        return t

    def t_literal_end(self, t):
        r'\n+\ *'
        column = find_column(t)
        indent = self.indent_stack[-1]
        if column < indent:
            # TODO rollback and dedent
            raise Exception('TODO, dedent')
        elif column == indent:
            t.lexer.pop_state()
            t.type = 'LITERAL_INDICATOR_END'
            return t
        else:
            t.type = 'SCALAR'
            return t

    # state: fold
    # -------------------------------------------------------------------
    t_fold_SCALAR = r'.+'

    def t_begin_fold(self, t):
        r'\ *(?<!\\)\>\ ?\n'
        t.lexer.push_state('fold')
        t.type = 'FOLD_INDICATOR_START'
        return t

    def t_fold_end(self, t):
        r'\n+\ *'
        column = find_column(t)
        indent = self.indent_stack[-1]
        if column < indent:
            # TODO rollback and dedent
            raise Exception('TODO, dedent')
        elif column == indent:
            t.lexer.pop_state()
            t.type = 'FOLD_INDICATOR_END'
            return t
        else:
            t.type = 'SCALAR'
            return t

    # state: INITIAL
    # -------------------------------------------------------------------
    t_ignore_EOL = r'\s*\n'

    def t_DOC_START_INDICATOR(self, t):
        r'\-\-\-'
        stack_length = len(self.doc_context_stack)
        if stack_length == 1:
            t.lexer.input('...' + t.lexer.lexdata[t.lexpos:])
            return t.lexer.token()
        elif stack_length == 0:

            self.doc_context_stack.append({})
            return t

    def t_DOC_END_INDICATOR(self, t):
        r'\.\.\.'
        self.doc_context_stack.pop()
        return t

    def t_SEQUENCE_INDICATOR(self, t):
        r'-\ '
        return t

    def t_MAP_INDICATOR(self, t):
        r':\ *'
        return t

    def t_SCALAR(self, t):
        r'(?:\\.|-(?!\ +)|[^\n\#\:\-\|])+'
        return t


def strict(*types):
    def decorate(func):
        @wraps(func)
        def wrapper(self, p):
            try:
                return func(self, p)
            finally:
                if not isinstance(p[0], types):
                    raise YAMLStrictTypeError(p[0], types, func)

        wrapper.co_firstlineno = func.__code__.co_firstlineno
        return wrapper

    return decorate


class YAMLProductions(TokenList):
    # PARSER
    # ===================================================================
    @strict(Docs)
    def p_docs_last(self, p):
        """
        docs    : DOC_START_INDICATOR doc DOC_END_INDICATOR
                | DOC_START_INDICATOR doc
        """
        p[0] = Docs(p[2])

    @strict(Docs)
    def p_docs_init(self, p):
        """
        docs    : docs DOC_START_INDICATOR doc DOC_END_INDICATOR
                | docs DOC_START_INDICATOR doc
        """
        p[0] = p[1] + Docs(p[3])

    @strict(Docs)
    def p_docs_implicit_single(self, p):
        """
        docs    : doc
        """
        p[0] = Docs(p[1])

    @strict(Doc)
    def p_doc_indent(self, p):
        """
        doc : INDENT doc DEDENT
        """
        p[0] = p[2]

    @strict(Doc)
    def p_doc(self, p):
        """
        doc : collection
            | scalar
        """
        p[0] = Doc(p[1])

    @strict(Collection)
    def p_collection(self, p):
        """
        collection  : sequence
                    | map
        """
        p[0] = p[1]

    @strict(Map)
    def p_map_last(self, p):
        """
        map : map_item
        """
        p[0] = Map(p[1])

    @strict(Map)
    def p_map_init(self, p):
        """
        map : map map_item
        """
        p[0] = p[1] + Map(p[2])

    def p_map_item(self, p):
        """
        map_item    : scalar MAP_INDICATOR scalar
        """
        p[0] = p[1], p[3]

    @strict(Sequence)
    def p_sequence_last(self, p):
        """
        sequence    : sequence_item
        """
        p[0] = Sequence(p[1])

    @strict(Sequence)
    def p_sequence_init(self, p):
        """
        sequence    : sequence sequence_item
        """
        p[0] = p[1] + Sequence(p[2])

    @strict(Scalar)
    def p_sequence_item(self, p):
        """
        sequence_item   : SEQUENCE_INDICATOR scalar
        """
        p[0] = p[2]

    @strict(Scalar)
    def p_scalar_explicit_cast(self, p):
        """
        scalar  : CAST_TYPE scalar
        """
        p[0] = ScalarDispatch(p[2].raw_value, cast=p[1])

    @strict(Scalar)
    def p_scalar(self, p):
        """
        scalar  : SCALAR
        """
        p[0] = ScalarDispatch(p[1])

    @strict(Str)
    def p_scalar_literal(self, p):
        """
        scalar  : LITERAL_INDICATOR_START scalar_group LITERAL_INDICATOR_END
        """
        p[0] = ScalarDispatch(dedent(p[2]).rstrip('\n'), cast='str')

    @strict(Str)
    def p_scalar_folded(self, p):
        """
        scalar  : FOLD_INDICATOR_START scalar_group FOLD_INDICATOR_END
        """

        cleaned_scalar = fold(dedent(p[2]).rstrip('\n'))
        p[0] = ScalarDispatch(cleaned_scalar, cast='str')

    @strict(str)
    def p_scalar_group(self, p):
        """
        scalar_group    : SCALAR
                        | scalar_group SCALAR
        """
        if len(p) == 2:
            p[0] = str(p[1])

        if len(p) == 3:
            p[0] = p[1] + p[2]

            #
            #   @strict(Null)
            #   def p_scalar_empty(self, p):
            #       """
            #       scalar  : empty
            #       """
            #       p[0] = ScalarDispatch('', cast='null')
            #
            #   def p_empty(self, p):
            #       """
            #       empty   :
            #       """
            #       pass
