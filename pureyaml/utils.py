#!/usr/bin/env python
# coding=utf-8
from contextlib import contextmanager


class ContextStack(object):
    def __init__(self, this=None):
        if this:
            init = {'self': this}
        else:
            init = {}
        self.__dict__['stack'] = [init]

    @property
    def attrs(self):
        return self.__dict__['stack'][-1]

    def __getattr__(self, item):
        return self.attrs[item]

    def __setattr__(self, key, value):
        self.attrs[key] = value

    def __getitem__(self, item):
        return self.attrs[item]

    def push(self, this):
        self.__dict__['stack'].append({'self': this})

    def pop(self):
        self.__dict__['stack'].pop()

    @contextmanager
    def context(self):
        self.push(self.self)
        yield
        self.pop()
