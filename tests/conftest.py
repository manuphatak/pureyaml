#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import logging

from pytest import fixture

from tests.utils import get_node_diff, init_logger


@fixture(scope='session', autouse=True)
def create_tabs():
    # from pureyaml.parser import YAMLLexer
    #
    # YAMLLexer.build(optimize=True)
    pass


@fixture(scope='session', autouse=True)
def setup_session():
    init_logger()
    logger = logging.getLogger('pureyaml')
    logger.info('Logger initiated from %s' % __file__)


def pytest_assertrepr_compare(op, left, right):
    from pureyaml.nodes import Node

    if isinstance(left, Node) and isinstance(right, Node) and op == '==':
        return ['Comparing Nodes'] + list(get_node_diff(left, right))
