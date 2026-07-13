#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import pytest
import iter_tokens as T
import node as N


class Parser:
    def __init__(self):
        self.tokens: Iterator[T.Token] = iter([])
        self.token: T.Token = T.Token("EOF")

    def _next(self, tokens: Iterator[T.Token]) -> T.Token:
        tok: T.Token = next(self.tokens)
        # print(f"_next {tok = }")
        return tok

    def _advance(self) -> T.Token:
        self.token = self._next(self.tokens)
        return self.token

    def _expect(self, expected: T.Token) -> None:
        if self.token != expected:
            raise SyntaxError(f"Expected {expected}, got {self.token}")
        self._consume()

    def _consume(self) -> None:
        try:
            self.token = self._next(self.tokens)
        except StopIteration:
            self.token = T.Token("EOF")

    def expr(self) -> N.Node:
        res: N.Node = self.term()
        while (op := self.token) != "EOF" and op in ("+", "-"):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == "+" else N.Minus(res, right)
        return res

    def term(self) -> N.Node:
        res: N.Node = self.factor()
        while (op := self.token) != "EOF" and op in ("*", "/"):
            self._consume()
            right = self.factor()
            res = N.Mul(res, right) if op == "*" else N.Div(res, right)
        return res

    def factor(self) -> N.Node:
        res: N.Node
        if self.token == "(":
            self._consume()
            res = self.expr()
            self._expect(T.Token("RPAREN", ")"))
        else:
            res = N.Num(float(self.token.val))
            self._consume()
        return res

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        return self.expr()


@pytest.mark.parametrize(
    ("sexpr", "expected"),
    [
        ["2 + 3", N.Plus(N.Num(2.0), N.Num(3.0))],
        ["3 / 4", N.Div(N.Num(3.0), N.Num(4.0))],
        ["2 + (3) + 4", N.Plus(N.Plus(N.Num(2.0), N.Num(3.0)), N.Num(4.0))],
        [
            "2 + (3 * 4) + 5",
            N.Plus(N.Plus(N.Num(2.0), N.Mul(N.Num(3.0), N.Num(4.0))), N.Num(5.0)),
        ],
    ],
)
def test_parser_basic(sexpr, expected):
    # sexpr = "2 + 3"
    # expected = N.Plus(N.Num(2.0), N.Num(3.0))
    assert Parser().parse(sexpr) == expected


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    print(n)
