#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from pureyaml.nodes import Node
from tests.utils import get_node_diff


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Node) and isinstance(right, Node) and op == '==':
        return ['Comparing Nodes'] + list(get_node_diff(left, right))
