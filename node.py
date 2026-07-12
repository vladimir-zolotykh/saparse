#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    def __init__(self, val):
        self.val = val


class Num(Node):
    pass


class BinOp(Node):
    def __init__(self, val, left, right):
        super().__init__(val)
        self.left = left
        self.right = right


class Plus(BinOp):
    def __init__(self, left, right):
        super().__init__("+", left, right)


class Minus(BinOp):
    def __init__(self, left, right):
        super().__init__("+", left, right)


class Mul(BinOp):
    def __init__(self, left, right):
        super().__init__("*", left, right)


class Div(BinOp):
    def __init__(self, left, right):
        super().__init__("/", left, right)
