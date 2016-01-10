#!/usr/bin/env python
# coding=utf-8
import os


def test_dir(*paths):
    dirname = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(dirname, *paths))
