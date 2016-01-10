#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

import os

from pytest import mark


def test_dir(*paths):
    dirname = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(dirname, *paths))


feature_not_supported = mark.skipif(True, reason='Feature not supported.')
