#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import iter_tokens as T
import node as N


class Parser:
    def __init__(self):
        self.tokens: Iterator[T.Token] = iter()

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

    def expr(self) -> N.Node:
        res = self.term()
        while (op := self.token) and op in ("+", "-"):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == "+" else N.Minus(res, right)
        return res

    def term(self) -> N.Node:
        res = self.factor()
        while (op := self.token) and op in ("*", "/"):
            self._consume()
            right = self.factor
            res = N.Mul(res, right) if op == "*" else N.Div(res, right)
        return res

    def factor(self) -> N.Node:
        if self.token == "(":
            self._consume()
            res = self.expr()
            self._expect(")")
        else:
            res = N.Num(self.token)
            self._consume()
        return res

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    print(n)
