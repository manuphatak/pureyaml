# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from .nodes import *  # noqa


class TokenList(object):
    tokens = [  # :off
        'DOC_START_INDICATOR',
        'DOC_END_INDICATOR',
        'SEQUENCE_INDICATOR',
        'MAP_INDICATOR',
        'CAST_TYPE',
        'SCALAR',
        'LITERAL_LINE',
        'INDENT',
        'DEDENT',
        'NODENT',
    ]  # :on


class YAMLTokens(TokenList):
    def __init__(self):
        self.indent_stack = [0]

    # LEXER
    # ===================================================================
    states = (  # :off
        ('tag', 'inclusive'),
        ('doublequote', 'exclusive'),
        ('commentstate', 'exclusive'),
        ('singlequote', 'exclusive'),
        # ('literal', 'exclusive'),

    )  # :on

    # state: multiple
    # -------------------------------------------------------------------
    def t_ignore_INDENT(self, t):
        r'\n\ *'
        # strip newline
        t.value = t.value[1:]

        indent_stack = self.indent_stack

        assert indent_stack == sorted(indent_stack)

        next_indent_length, curr_indent_length = len(t.value), self.indent_stack[-1]
        if next_indent_length > curr_indent_length:
            indent_stack.append(next_indent_length)
            t.type = 'INDENT'
            return t

        elif next_indent_length == curr_indent_length:
            # t.type = 'NODENT'
            pass
        else:
            prev_indent_length = indent_stack.pop()
            t.lexer.lexpos -= curr_indent_length - prev_indent_length

            t.type = 'DEDENT'
            return t

    # state: tag
    # -------------------------------------------------------------------
    def t_begin_tag(self, t):
        r'(?<!\\)!'
        t.lexer.push_state('tag')
        t.lexer.begin('tag')

    def t_tag_end(self, t):
        r'\ '
        t.lexer.begin('INITIAL')

    def t_tag_CAST_TYPE(self, t):
        r'(?<=\!)[a-z]+'
        return t

    # state: doublequote
    # -------------------------------------------------------------------
    t_doublequote_SCALAR = r'(?:\\"|[^"])+'

    def t_begin_doublequote(self, t):
        r'(?<!\\)"'
        t.lexer.begin('doublequote')
        t.type = 'CAST_TYPE'
        t.value = 'str'
        return t

    def t_doublequote_end(self, t):
        r'(?<!\\)"'
        t.lexer.begin('INITIAL')

    # state: commentstate
    # -------------------------------------------------------------------
    t_commentstate_ignore_COMMENT = r'[^\n]+'

    def t_begin_commentstate(self, t):
        r'\s*\#\ ?'
        t.lexer.begin('commentstate')

    def t_commentstate_end(self, t):
        r'(?=\n)'
        t.lexer.begin('INITIAL')

    # state: singlequote
    # -------------------------------------------------------------------

    t_singlequote_SCALAR = r"(?:\\'|[^'])+"

    def t_begin_singlequote(self, t):
        r"(?<!\\)'"
        t.lexer.begin('singlequote')
        t.type = 'CAST_TYPE'
        t.value = 'str'
        return t

    def t_singlequote_end(self, t):
        r"(?<!\\)'"
        t.lexer.begin('INITIAL')

    #
    # # state: literal
    # # -------------------------------------------------------------------
    #
    # def t_literal_LITERAL_LINE(self, t):
    #     r'[\w\s]+'
    #     return t
    #
    #
    # def t_begin_literal(self, t):
    #     r'(?<!\\)\|'
    #     t.lexer.push_state('literal')
    #
    #
    # def t_literal_end(self, t):
    #     r'\n\n'
    #     t.lexer.pop_state()

    # state: INITIAL
    # -------------------------------------------------------------------
    t_ignore_EOL = r'\s*\n'

    def t_DOC_START_INDICATOR(self, t):
        r'\-\-\-'
        return t

    def t_DOC_END_INDICATOR(self, t):
        r'\.\.\.'
        return t

    def t_SEQUENCE_INDICATOR(self, t):
        r'-\ '
        return t

    def t_MAP_INDICATOR(self, t):
        r':\ *'
        return t

    def t_SCALAR(self, t):
        r'(?:\\.)|[^\n\#\:\-]+'
        return t


class YAMLProductions(TokenList):
    # PARSER
    # ===================================================================

    def p_docs_last(self, p):
        """
        docs    : DOC_START_INDICATOR doc DOC_END_INDICATOR
                | DOC_START_INDICATOR doc
        """
        p[0] = Docs(p[2])

    def p_docs_init(self, p):
        """
        docs    : docs DOC_START_INDICATOR doc DOC_END_INDICATOR
                | docs DOC_START_INDICATOR doc
        """
        p[0] = p[1] + Docs(p[3])

    def p_docs_implicit_single(self, p):
        """
        docs    : doc
        """
        p[0] = p[1]

    def p_doc_indent(self, p):
        """
        doc : INDENT doc DEDENT
        """
        p[0] = p[2]

    def p_doc(self, p):
        """
        doc : collection
            | scalar
        """
        p[0] = Doc(p[1])


    def p_collection(self, p):
        """
        collection  : sequence
                    | map
        """
        p[0] = p[1]

        if not isinstance(p[0], Collection):
            raise TypeError

    def p_map_last(self, p):
        """
        map : map_item
        """
        p[0] = Map(p[1])

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

    def p_sequence_last(self, p):
        """
        sequence    : sequence_item
        """
        p[0] = Sequence(p[1])

    def p_sequence_init(self, p):
        """
        sequence    : sequence sequence_item
        """
        p[0] = p[1] + Sequence(p[2])

    def p_sequence_item(self, p):
        """
        sequence_item   : SEQUENCE_INDICATOR scalar
        """
        p[0] = p[2]

    def p_scalar_explicit_cast(self, p):
        """
        scalar  : CAST_TYPE scalar
        """
        p[0] = ScalarDispatch(p[2].raw_value, cast=p[1])

    def p_scalar_string(self, p):
        """
        scalar  : SCALAR
        """
        p[0] = ScalarDispatch(p[1])

        # def p_scalar_literal(self, p):
        #     """
        #     scalar  : literal_lines
        #     """
        #     p[0] = p[1]

        # def p_literal_lines(self, p):
        #     """
        #     literal_lines   : LITERAL_LINE
        #     """
        #     p[0] = p[1]
