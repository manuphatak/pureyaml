# coding=utf-8
"""
pureyaml
"""
from __future__ import absolute_import

import re
from textwrap import dedent

from .tokens import YAMLTokens
from .utils import strict, fold
from ..nodes import *  # noqa


# noinspection PyIncorrectDocstring
class YAMLProductions(YAMLTokens):
    # PARSER
    # ===================================================================
    @strict(Docs)
    def p_docs__last(self, p):
        """
        docs    : doc
                | doc DOC_END
        """
        p[0] = Docs(p[1])

    @strict(Docs)
    def p_docs__init(self, p):
        """
        docs    : docs doc
        """
        p[0] = p[1] + Docs(p[2])

    @strict(Doc)
    def p_doc__indent(self, p):
        """
        doc : DOC_START doc DOC_END
            | DOC_START doc
            | INDENT doc DEDENT
        """
        p[0] = p[2]

    @strict(Doc)
    def p_doc(self, p):
        """
        doc : collection
            | scalar
        """
        p[0] = Doc(p[1])

    @strict(Sequence, Map)
    def p_collection(self, p):
        """
        collection  : sequence
                    | map
                    | flow_collection
        """
        p[0] = p[1]

    @strict(Map)
    def p_map__last(self, p):
        """
        map : map_item
        """
        p[0] = Map(p[1])

    @strict(Map)
    def p_map__init(self, p):
        """
        map : map map_item
        """
        p[0] = p[1] + Map(p[2])

    @strict(tuple)
    def p_map_item(self, p):
        """
        map_item    : map_item_key map_item_value
        """
        p[0] = p[1], p[2]

    @strict(tuple)
    def p_map_item__compact_scalar(self, p):
        """
        map_item    : B_MAP_COMPACT_KEY scalar B_MAP_VALUE scalar DEDENT
        """
        p[0] = p[2], p[4]

    @strict(Scalar)
    def p_map_item_key__complex_key_scalar(self, p):
        """
        map_item_key    : B_MAP_KEY         scalar
        """
        p[0] = p[2]

    @strict(Scalar)
    def p_map_item_key(self, p):
        """
        map_item_key    : scalar
        """
        p[0] = p[1]

    @strict(Map, Sequence)
    def p_map_item___key_value__collection(self, p):
        """
        map_item_key    :  B_MAP_KEY    INDENT collection DEDENT
        map_item_value  :  B_MAP_VALUE  INDENT collection DEDENT
        """
        p[0] = p[3]

    @strict(Map, Sequence)
    def p_map_item_value__flow_collection(self, p):
        """
        map_item_value  :  B_MAP_VALUE flow_collection
        """
        p[0] = p[2]

    @strict(Scalar)
    def p_map_item_value__scalar(self, p):
        """
        map_item_value  : B_MAP_VALUE scalar
        """
        p[0] = p[2]

    @strict(Sequence)
    def p_map_item_value__sequence_no_indent(self, p):
        """
        map_item_value  : B_MAP_VALUE sequence
        """
        p[0] = p[2]

    # @strict(Null)
    # def p_map_item_value_empty(self, p):
    #     """
    #     map_item_value  : B_MAP_VALUE empty
    #     """
    #     p[0] = Null(None)

    @strict(Sequence)
    def p_sequence__last(self, p):
        """
        sequence    : sequence_item
        """
        p[0] = Sequence(p[1])

    @strict(Sequence)
    def p_sequence__init(self, p):
        """
        sequence    : sequence sequence_item
        """
        p[0] = p[1] + Sequence(p[2])

    @strict(Scalar)
    def p_sequence_item__scalar(self, p):
        """
        sequence_item   : B_SEQUENCE_START scalar
        """
        p[0] = p[2]

    # @strict(Null)
    # def p_sequence_item_scalar_empty(self, p):
    #     """
    #     sequence_item   : B_SEQUENCE_START empty
    #     """
    #     p[0] = Null(None)

    @strict(Map, Sequence)
    def p_sequence_item__collection(self, p):
        """
        sequence_item   : B_SEQUENCE_START INDENT collection DEDENT
        """
        p[0] = p[3]

    @strict(Map, Sequence)
    def p_map_item__key__map_item_value__sequence_item__compact_collection(self, p):
        """
        map_item_key    : B_MAP_COMPACT_KEY         collection DEDENT
        map_item_value  : B_MAP_COMPACT_VALUE       collection DEDENT
        sequence_item   : B_SEQUENCE_COMPACT_START  collection DEDENT
        """
        p[0] = p[2]

    @strict(Map, Sequence)
    def p_sequence_item__flow_collection(self, p):
        """
        sequence_item   : B_SEQUENCE_START flow_collection
        """
        p[0] = p[2]

    @strict(Str)
    def p_scalar__doublequote(self, p):
        """
        scalar  : DOUBLEQUOTE_START SCALAR DOUBLEQUOTE_END
        """
        scalar = re.sub('\n\s+', ' ', str(p[2]))
        p[0] = Str(scalar.replace('\\"', '"'))

    @strict(Str)
    def p_scalar__singlequote(self, p):
        """
        scalar  : SINGLEQUOTE_START SCALAR SINGLEQUOTE_END
        """
        p[0] = Str(str(p[2]).replace("''", "'"))

    @strict(Str)
    def p_scalar__quote_empty(self, p):
        """
        scalar  : DOUBLEQUOTE_START DOUBLEQUOTE_END
                | SINGLEQUOTE_START SINGLEQUOTE_END
        """
        p[0] = Str('')

    @strict(Scalar)
    def p_scalar__explicit_cast(self, p):
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
    def p_scalar__literal(self, p):
        """
        scalar  : B_LITERAL_START scalar_group B_LITERAL_END
        """
        scalar_group = ''.join(p[2])
        p[0] = ScalarDispatch('%s\n' % dedent(scalar_group).replace('\n\n\n', '\n'), cast='str')

    @strict(Str)
    def p_scalar__folded(self, p):
        """
        scalar  : B_FOLD_START scalar_group B_FOLD_END
        """
        scalar_group = ''.join(p[2])
        cleaned_scalar = fold(dedent(scalar_group)).rstrip()
        p[0] = ScalarDispatch('%s\n' % cleaned_scalar, cast='str')

    @strict(Str)
    def p_scalar__indented_flow(self, p):
        """
        scalar  : INDENT scalar_group DEDENT
        """
        scalar_group = '\n'.join(p[2])
        cleaned_scalar = fold(dedent(scalar_group))
        p[0] = ScalarDispatch(cleaned_scalar, cast='str')

    @strict(tuple)
    def p_scalar_group(self, p):
        """
        scalar_group    : SCALAR
                        | scalar_group SCALAR
        """
        if len(p) == 2:
            p[0] = (str(p[1]),)

        if len(p) == 3:
            p[0] = p[1] + (str(p[2]),)

    @strict(Sequence, Map)
    def p_flow_collection(self, p):
        """
        flow_collection : F_SEQUENCE_START flow_sequence F_SEQUENCE_END
                        | F_MAP_START flow_map F_MAP_END
        """
        p[0] = p[2]

    @strict(Sequence)
    def p_flow_sequence__last(self, p):
        """
        flow_sequence   : flow_sequence_item
        """
        p[0] = Sequence(p[1])

    @strict(Sequence)
    def p_flow_sequence__init(self, p):
        """
        flow_sequence   : flow_sequence F_SEP flow_sequence_item
        """
        p[0] = p[1] + Sequence(p[3])

    @strict(Scalar)
    def p_flow_sequence_item(self, p):
        """
        flow_sequence_item  : scalar
        """
        p[0] = p[1]

    @strict(Map)
    def p_flow_map__last(self, p):
        """
        flow_map   : flow_map_item
        """
        p[0] = Map(p[1])

    @strict(Map)
    def p_flow_map__init(self, p):
        """
        flow_map   : flow_map F_SEP flow_map_item
        """
        p[0] = p[1] + Map(p[3])

    @strict(tuple)
    def p_flow_map_item(self, p):
        """
        flow_map_item  : flow_map_item_key flow_map_item_value
        """
        p[0] = p[1], p[2]

    @strict(Scalar)
    def p_flow_map_item_key(self, p):
        """
        flow_map_item_key   : scalar F_MAP_KEY
        """
        p[0] = p[1]

    @strict(Scalar)
    def p_flow_map_item_value(self, p):
        """
        flow_map_item_value    : scalar
        """
        p[0] = p[1]

        # def p_empty(self, p):
        #     """empty    :"""
        #     pass
