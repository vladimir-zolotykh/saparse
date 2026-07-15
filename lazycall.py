#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from types import MethodType


class lazycall:
    def __init__(self, func):
        self.func = func
        self.cache = "_cache"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.cache not in instance.__dict__:
            instance.__dict__[self.cache] = {}
        return MethodType(self, instance)

    def __call__(self, *args):
        # args = (<__main__.Fib object at 0x7feb8a8242d0>, 6)
        instance, n = args
        if n not in instance.__dict__[self.cache]:
            val = self.func(*args)
            instance._cache[n] = val
        return instance._cache[n]


class Fib:
    @lazycall
    def fib(self, n):
        print(f"Calculating fibonacci({n})")
        return self.fib(n - 1) + self.fib(n - 2) if n >= 2 else n


if __name__ == "__main__":
    f = Fib()
    print(f.fib(7))
    print(f.fib(8))
