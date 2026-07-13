#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, Any, cast
import re
from enum import StrEnum, auto


class Symbol(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

    NAME = auto()
    NUM = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    WS = auto()
    EOF = auto()


# (?P<name>...)
Tokens: dict[str, str] = {
    t[0]: f"(?P<{t[0]}>{t[1]})"
    for t in (
        (Symbol.NAME, r"[A-Za-z_][A-Za-z_0-9]+"),
        (Symbol.NUM, r"\d+"),
        (Symbol.PLUS, r"\+"),
        (Symbol.MINUS, r"-"),
        (Symbol.MUL, r"\*"),
        (Symbol.DIV, r"/"),
        (Symbol.LPAREN, r"\("),
        (Symbol.RPAREN, r"\)"),
        (Symbol.WS, r"\s+"),
    )
}


class Token:
    # def __init__(self, name: str, val: str | float = "EOF"):
    def __init__(self, name: Symbol, val: str | float = ""):
        self.name = name
        self.val = val

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        elif isinstance(other, Symbol):
            return self.name == other
        else:
            return False

    def as_tuple(self):
        return ", ".join(f"{v!r}" for v in self.__dict__.values())

    def __repr__(self):
        return f"{type(self).__name__}({self.as_tuple()})"


def iter_tokens(sexpr: str) -> Iterator[Token]:
    pat = "|".join(Tokens.values())
    for match in re.finditer(pat, sexpr):
        # if match.lastgroup == "WS":
        if match.lastgroup == Symbol.WS:
            continue
        yield Token(cast(Symbol, match.lastgroup), match.group(0))


if __name__ == "__main__":
    sexpr = "3 + (4 * 5) + 6"
    for tok in iter_tokens(sexpr):
        print(tok)
