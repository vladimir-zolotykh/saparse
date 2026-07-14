#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import math


class lazyproperty:
    def __init__(self, func):
        self.func = func
        self._var = f"{func.__name__}_var"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if hasattr(instance, self._var):
            return getattr(instance, self._var)
        else:
            val = self.func(instance)
            setattr(instance, self._var, val)
            return val


class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    @lazyproperty
    def area(self):
        print("Calculating area")
        return math.pi * self.radius**2

    @lazyproperty
    def circumference(self):
        print("Calculating circumference")
        return 2.0 * math.pi * self.radius


if __name__ == "__main__":
    c = Circle(10.2)
    print(c.circumference)
    print(c.circumference)
