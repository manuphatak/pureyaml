# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

from pprint import pformat

from ply.lex import lex
from ply.yacc import yacc

from .nodes import *  # noqa


class TokenList(object):
    tokens = [  # :off
        'DOC_START_INDICATOR',
        'DOC_END_INDICATOR',
        'SEQUENCE_INDICATOR',
        'MAP_INDICATOR',
        'CAST_TYPE',
        'FLOAT',
        'INT',
        'BOOL',
        'SCALAR',
        'LITERAL_LINE',
        'INDENT',
        'DEDENT',
        'NODENT',
    ]  # :on


class YAMLLexer(TokenList):
    def __init__(self):
        self.indent_stack = [0]

    @classmethod
    def build(cls, **kwargs):
        self = cls()
        kwargs.setdefault('module', self)
        return lex(**kwargs)

    @classmethod
    def tokenize(cls, data):
        lexer = cls.build()
        lexer.input(data)
        while True:
            token = lexer.token()
            if not token:
                break
            yield token

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

    def t_ANY_error(self, t):
        raise SyntaxError(show_error(t, t.value[0]))

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
        r'\s*[\#]\ ?'
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

    t_ignore_EOL = r'\s*\n'

    def t_FLOAT(self, t):
        r'\d*\.\d+'
        return t

    def t_INT(self, t):
        r'\d+'
        return t

    def t_BOOL(self, t):
        r'Yes|No'
        return t

    def t_SCALAR(self, t):
        r'(?:\\.)|[\w\ ,!\\]+'
        return t


class YAMLParser(TokenList):
    def __init__(self, **kwargs):
        kwargs.setdefault('module', self)
        kwargs.setdefault('tabmodule', '_parsetab')
        kwargs.setdefault('debugfile', '_parser.out')
        self.debug = kwargs.get('debug')
        self.parser = yacc(**kwargs)

    def parse(self, data, **kwargs):
        kwargs.setdefault('lexer', YAMLLexer.build())
        return self.parser.parse(data, **kwargs)

    def parsedebug(self, data, **kwargs):
        print('')
        print(self.tokenize(data))
        kwargs.setdefault('lexer', YAMLLexer.build(debug=True))
        kwargs.setdefault('debug', True)

        return self.parser.parse(data, **kwargs)

    def tokenize(self, data):
        tokens = YAMLLexer.tokenize(data)
        return pformat(list(tokens))

    # PARSER
    # ===================================================================
    def p_docs_init(self, p):
        """
        docs    : DOC_START_INDICATOR doc DOC_END_INDICATOR docs
                | DOC_START_INDICATOR doc docs
        """

        if len(p) == 5:
            docs = p[4]
        else:
            docs = p[3]

        p[0] = Docs(p[2]) + docs

    # def p_docs_indent(self, p):
    #     """
    #     docs    : DOC_START_INDICATOR INDENT doc docs DEDENT DOC_END_INDICATOR
    #             | DOC_START_INDICATOR INDENT doc docs DEDENT
    #             | DOC_START_INDICATOR INDENT doc DEDENT DOC_END_INDICATOR
    #             | DOC_START_INDICATOR INDENT doc DEDENT
    #             | DOC_START_INDICATOR INDENT doc
    #     """
    #     if len(p) == 6 or len(p) == 7:
    #         p[0] = Docs(p[3]) + p[4]
    #
    #     elif len(p) == 4 or len(p) == 5:
    #         p[0] = Docs(p[3])

    def p_docs_last(self, p):
        """
        docs    : DOC_START_INDICATOR doc DOC_END_INDICATOR
                | DOC_START_INDICATOR doc
        """
        p[0] = Docs(p[2])

    def p_docs_implicit(self, p):
        """
        docs    : doc
        """
        p[0] = p[1]

    def p_doc(self, p):
        """
        doc : collection
            | scalar
        """
        p[0] = Doc(p[1])

    def p_doc_indent(self, p):
        """
        doc : INDENT collection DEDENT
            | INDENT collection
            | INDENT scalar DEDENT
            | INDENT scalar
        """
        p[0] = Doc(p[2])

    def p_collection(self, p):
        """
        collection  : sequence
                    | map
        """
        p[0] = p[1]

    def p_map_init(self, p):
        """
        map : map_item map
        """
        p[0] = Map(p[1]) + p[2]

    def p_map_last(self, p):
        """
        map : map_item
        """
        p[0] = Map(p[1])

    def p_map_item(self, p):
        """
        map_item    : scalar MAP_INDICATOR scalar
        """
        p[0] = p[1], p[3]

    def p_sequence_init(self, p):
        """
        sequence    : sequence_item sequence
        """
        p[0] = Sequence(p[1]) + p[2]

    def p_sequence_last(self, p):
        """
        sequence    : sequence_item
        """
        p[0] = Sequence(p[1])

    def p_sequence_item(self, p):
        """
        sequence_item   : SEQUENCE_INDICATOR scalar
        """
        p[0] = p[2]

    def p_scalar_explicit_cast(self, p):
        """
        scalar  : CAST_TYPE scalar
        """
        type_nodes = {'int': Int, 'str': Str, 'float': Float}
        p[0] = ScalarDispatch(p[2].value, cast=p[1])

    def p_scalar_float(self, p):
        """
        scalar  : FLOAT
        """

        p[0] = ScalarDispatch(p[1], cast='float')

    def p_scalar_int(self, p):
        """
        scalar  : INT
        """

        p[0] = ScalarDispatch(p[1], cast='int')

    def p_scalar_bool(self, p):
        """
        scalar  : BOOL
        """
        p[0] = ScalarDispatch(p[1], cast='bool')
    #
    # def p_scalar_literal(self, p):
    #     """
    #     scalar  : literal_lines
    #     """
    #     p[0] = p[1]

    def p_scalar_string(self, p):
        """
        scalar  : SCALAR
        """
        p[0] = ScalarDispatch(p[1])

    # def p_literal_lines(self, p):
    #     """
    #     literal_lines   : LITERAL_LINE
    #     """
    #     p[0] = p[1]

    def p_error(self, p):
        # guard, empty p
        if p is None:
            raise SyntaxError('Unknown origin %s' % p)

        raise SyntaxError(show_error(p, p.value))


class YAMLSyntaxError(SyntaxError):
    pass


def show_error(p, value):
    # setup
    show_chars = 30
    preview_start = max(0, p.lexpos - show_chars)
    preview_end = min(len(p.lexer.lexdata), p.lexpos + show_chars + 1)
    error_length = max(1, len(repr(value)[1:-1]))
    error_end = p.lexpos + error_length
    # line 3
    pre_error_text = p.lexer.lexdata[preview_start:p.lexpos]
    cur_error_text = p.lexer.lexdata[p.lexpos:error_end]
    suf_error_text = p.lexer.lexdata[error_end + 1:preview_end]

    # line 4
    width = len(repr(pre_error_text + cur_error_text)[1:-1])
    error_lines = [  # :off
        '\n',
        'Unexpected value: %r:%r' % (p.type, value),
        repr(pre_error_text + cur_error_text + suf_error_text)[1:-1],
        ('^' * error_length).rjust(width, ' '),
    ]  # :on
    return '\n'.join(error_lines)
