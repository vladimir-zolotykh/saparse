#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        cached = type(cls)._instances
        if cls not in cached:
            cached[cls] = super().__call__(*args, **kwargs)
        return cached[cls]


class Logger(metaclass=Singleton):
    def __init__(self):
        print(f"Initializing {self}")


class Module(metaclass=Singleton):
    def __init__(self):
        print(f"Initializing {self}")


if __name__ == "__main__":
    o1 = Logger()
    o2 = Logger()
    assert o1 is o2
    m1 = Module()
    m2 = Module()
    assert m1 is m2
    assert o1 is not m1
