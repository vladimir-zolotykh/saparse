#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
from types import MethodType
from inspect import signature
from functools import wraps
import node as N
import parser as P


class MultiMethod:
    def __init__(self, name):
        self._name = name
        self.methods: dict[tuple[type, ...], Callable] = {}

    def register(self, func):
        sig = signature(func)
        tup: tuple[type, ...] = tuple(
            p.annotation for n, p in sig.parameters.items() if n != "self"
        )
        self.methods[tup] = func

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        tup: tuple[type, ...] = tuple(type(a) for a in args[1:])
        return self.methods[tup](*args, **kwargs)


class MultiDict(dict):
    def __setitem__(self, key: str, val: object) -> None:
        if (key[:2] == "__" and key[-2:] == "__") or (key not in self):
            super().__setitem__(key, val)
            return
        oval = self[key]
        if isinstance(oval, MultiMethod):
            mm = oval
            mm.register(val)
        else:
            mm = MultiMethod(key)
            mm.register(oval)
            mm.register(val)
        super().__setitem__(key, mm)


class MultiMeta(type):
    @classmethod
    def __prepare__(mcls, clsname, bases, /, **kwargs):
        return MultiDict()


def dots(func):
    name = func.__name__

    @wraps(func)
    def wrapper(self, n):
        depth = getattr(self, "_depth", 0)
        # print("." * depth, f"{name}({n})")
        print(f"{'.' * depth}{name}({n})")
        self._depth = depth + 4
        res = func(self, n)
        # print("." * depth, f"->{res!r}")
        print(f"{'.' * depth}->{res!r}")
        return res

    return wrapper


class Visitor(metaclass=MultiMeta):
    @dots
    def visit(self, n: N.Num) -> float:
        return float(n.val)

    @dots
    def visit(self, n: N.Plus) -> float:  # noqa: F811
        return self.visit(n.left) + self.visit(n.right)

    @dots
    def visit(self, n: N.Minus) -> float:  # noqa: F811
        return self.visit(n.left) - self.visit(n.right)

    @dots
    def visit(self, n: N.Mul) -> float:  # noqa: F811
        return self.visit(n.left) * self.visit(n.right)

    @dots
    def visit(self, n: N.Div) -> float:  # noqa: F811
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = P.Parser().parse(sexpr)
    print(Visitor().visit(n))
