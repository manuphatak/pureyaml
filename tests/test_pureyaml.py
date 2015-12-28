#!/usr/bin/env python
# coding=utf-8

"""
test_pureyaml
----------------------------------

Tests for `pureyaml` module.
"""
from pytest import fixture

@fixture
def boilerplate():
    from pureyaml.pureyaml import Boilerplate

    return Boilerplate()


def test_cookiecutter_automates_boilerplate(boilerplate):
    assert str(boilerplate) == "Success"
