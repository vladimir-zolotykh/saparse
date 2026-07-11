#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re


class _Re:
    pass


# (?P<name>...)
TOKENS: dict[str, re.Pattern] = {
    t[0]: f"(?P<{t[0]}>{t[1]})"
    for t in (
        ("NAME", r"[A-Za-z_][A-Za-z_0-9]+"),
        ("NUM", r"\d+"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
    )
}


class Token:
    def __init__(self, name: str, val: str | float):
        self.name = name
        self.val = val

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def as_tuple(self):
        return ", ".join(f"{v!r}" for v in self.__dict__.values())

    def __repr__(self):
        return f"{type(self).__name__}({self.as_tuple()})"


def iter_tokens(sexpr: str) -> Iterator[Token]:
    pat = "|".join(TOKENS.values())
    for match in re.finditer(pat, sexpr):
        if match.lastgroup == "WS":
            continue
        yield Token(match.lastgroup, match.group(0))


if __name__ == "__main__":
    sexpr = "3 + (4 * 5) + 6"
    for tok in iter_tokens(sexpr):
        print(tok)
