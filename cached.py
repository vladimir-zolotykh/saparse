#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    cached = defaultdict(defaultdict)

    def __call__(cls, *args, **kwargs):
        key = tuple(args)
        if cls not in (cached := type(cls).cached) or key not in cached[cls]:
            cached[cls][key] = super().__call__(*args, **kwargs)
        return cached[cls][key]


class Person(metaclass=CachedMeta):
    def __init__(self, name, age, salary):
        print(f"Initializing {type(self).__name__} object of {name!r}")
        self.name = name
        self.age = age
        self.salary = salary

    def _as_tuple(self) -> tuple[type, ...]:
        return tuple(a for a in self.__dict__.values())

    def __repr__(self):
        args = ", ".join(repr(x) for x in self._as_tuple())
        return f"{type(self).__name__}({args})"


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
    leo = Person("Leo", 42, 48000)
    bob = Person("Bob", 37, 12000)
    bob = Person("Bob", 38, 12000)
