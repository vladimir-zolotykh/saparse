#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
from functools import wraps
import iter_tokens as T
import node as N


def trace_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__
        print(f"{name} >>>")
        res = func(*args, **kwargs)
        print(f"<<< {res}")
        return res

    return wrapper


class Parser:
    def __init__(self):
        self.tokens: Iterator[T.Token] = iter([])
        self.token: T.Token = None

    def _advance(self) -> T.Token:
        self.token = next(self.tokens)

    def _expect(self, expected: T.Token) -> None:
        if self.token != expected:
            raise SyntaxError(f"Expected {expected}, got {self.token}")
        self._consume()

    def _consume(self) -> None:
        try:
            self._advance()
        except StopIteration:
            self.token = None

    @trace_func
    def expr(self) -> N.Node:
        res: N.Node = self.term()
        while (op := self.token) and op in ("+", "-"):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == "+" else N.Minus(res, right)
        return res

    @trace_func
    def term(self) -> N.Node:
        res: N.Node = self.factor()
        while (op := self.token) and op in ("*", "/"):
            self._consume()
            right = self.factor
            res = N.Mul(res, right) if op == "*" else N.Div(res, right)
        return res

    @trace_func
    def factor(self) -> N.Node:
        res: N.Node
        if self.token == "(":
            self._consume()
            res = self.expr()
            self._expect(")")
        else:
            res = N.Num(float(self.token.val))
            self._consume()
        return res

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    # sexpr = "2 + (3 * 4) + 5"
    sexpr = "2 + 3"
    n: N.Node = Parser().parse(sexpr)
    print(n)
