import math
from abc import ABCMeta, abstractmethod


class Operator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_string(self, left, right):
        return ''

    @abstractmethod
    def evaluate(self, left, right):
        pass


class Add(Operator):
    def to_string(self, left, right):
        return '(%s + %s)' % (left, right)

    def evaluate(self, left, right):
        try:
            return left + right
        except OverflowError:
            return 0


class BAnd(Operator):
    def to_string(self, left, right):
        return '(int(%s) & int(%s))' % (left, right)

    def evaluate(self, left, right):
        return int(left) & int(right)


class BOr(Operator):
    def to_string(self, left, right):
        return '(int(%s) | int(%s))' % (left, right)

    def evaluate(self, left, right):
        return int(left) | int(right)


class Div(Operator):
    def to_string(self, left, right):
        return '(%s / %s)' % (left, right)

    def evaluate(self, left, right):
        return left / right if right else 0


class Mul(Operator):
    def to_string(self, left, right):
        return '(%s * %s)' % (left, right)

    def evaluate(self, left, right):
        try:
            return left * right
        except OverflowError:
            return 0


class Pow(Operator):
    def to_string(self, left, right):
        return '(%s ** %s)' % (left, right)

    def evaluate(self, left, right):
        try:
            return left ** right
        except:
            return 0


class Sub(Operator):
    def to_string(self, left, right):
        return '(%s - %s)' % (left, right)

    def evaluate(self, left, right):
        try:
            return left - right
        except OverflowError:
            return 0


class Xor(Operator):
    def to_string(self, left, right):
        return '(int(%s) ^ int(%s))' % (left, right)

    def evaluate(self, left, right):
        return int(left) ^ int(right)


class Sin(Operator):
    def to_string(self, left, right=None):
        return 'sin(%s)' % left

    def evaluate(self, left, right=None):
        return math.sin(left)


class Cos(Operator):
    def to_string(self, left, right=None):
        return 'cos(%s)' % left

    def evaluate(self, left, right=None):
        return math.cos(left)


class Tan(Operator):
    def to_string(self, left, right=None):
        return 'tan(%s)' % left

    def evaluate(self, left, right=None):
        return math.tan(left)


class Bin(Operator):
    def to_string(self, left, right=None):
        return 'bin(%s)' % left

    def evaluate(self, left, right=None):
        n = bin(int(left))
        return int(n[3:])*-1 if n[0] == '-' else int(n[2:])
