#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import node as N
import parser as P
from functools import singledispatchmethod


class Visitor:
    @singledispatchmethod
    def visit(self, n: N.Node) -> float:
        raise NotImplementedError("Cannot negate a")

    @visit.register
    def _(self, n: N.Num) -> float:
        return float(n.val)

    @visit.register
    def _(self, n: N.Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    @visit.register
    def _(self, n: N.Minus) -> float:
        return self.visit(n.left) - self.visit(n.right)

    @visit.register
    def _(self, n: N.Mul) -> float:
        return self.visit(n.left) * self.visit(n.right)

    @visit.register
    def _(self, n: N.Div) -> float:
        return self.visit(n.left) / self.visit(n.right)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = P.Parser().parse(sexpr)
    print(Visitor().visit(n))
