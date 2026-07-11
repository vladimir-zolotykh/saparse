#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    cached = defaultdict(defaultdict())

    def __call__(cls, *args, **kwargs):
        # cached = type(cls).cached
        key = tuple(args)
        if cls not in (cached := type(cls).cached) and key not in cached[cls]:
            cached[cls][key] = super().__call__(*args, **kwargs)
        return cached[cls][key]


class Person(metaclass=CachedMeta):
    def __init__(self, name, age, salary):
        print(f"Initializing {type(self).__name__} object")
        self.name = name
        self.age = age
        self.salary = salary

    def _as_tuple(self):
        return tuple()

    def __repr__(self):
        return f"{type(self).__name__}(self._as_tuple())"


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    leo = Person("Leo", 42, 48000)
    bob = Person("Bob", 37, 12000)
    bob = Person("Bob", 38, 12000)
