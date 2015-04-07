import math
from abc import ABCMeta, abstractmethod
from ..tools import rand_int, rand_double, mutate
from .operators import *


class MathLiteral(object):
    __metaclass__ = ABCMeta

    def __str__(self):
        return 'FEL'

    def create_random_node(self):
        types = [
            MathOp,
            MathValue,
            MathPi,
            MathVariable,
        ]

        index = rand_int(len(types))
        literal = types[index]()
        return literal

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def evaluate(self, engine):
        pass

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def is_static(self):
        pass


class MathPi(MathLiteral):
    value = 0.0

    def __init__(self):
        self.value = math.pi

    def __str__(self):
        return 'pi'

    def mutate(self):
        pass

    def evaluate(self, engine):
        return self.value

    def clone(self):
        clone = MathPi()
        clone.value = self.value
        return clone

    def is_static(self):
        return True


class MathValue(MathLiteral):
    value = 0.0

    def __init__(self):
        self.mutate_value()

    def __str__(self):
        return '%s' % self.value

    def mutate_value(self):
        noise = (rand_double() - 0.5) * 10
        self.value += noise

    def mutate(self):
        if mutate(50):
            self.mutate_value()

        if mutate(100):
            digits = rand_int(5)
            self.value = round(self.value, digits)

        if mutate(200):
            self.value = int(self.value)

    def evaluate(self, engine):
        return self.value

    def clone(self):
        clone = MathValue()
        clone.value = self.value
        return clone

    def is_static(self):
        return True


class MathVariable(MathLiteral):
    name = ''

    def __init__(self):
        self.mutate_variable()

    def __str__(self):
        return '%s' % self.name

    def mutate_variable(self):
        variables = 'xy'
        index = rand_int(len(variables))
        self.name = '%s' % variables[index]

    def mutate(self):
        if mutate(20):
            self.mutate_variable()

    def evaluate(self, engine):
        return engine.get_variable(self.name)

    def clone(self):
        clone = MathVariable()
        clone.name = self.name
        return clone

    def is_static(self):
        return False


class MathOp(MathLiteral):
    operators = None
    left = None
    right = None
    operator = None

    def __init__(self):
        self.operators = self.get_operators()

        self.mutate_op()
        self.left = MathValue()
        self.right = MathValue()

    def __str__(self):
        return self.operator.to_string(str(self.left), str(self.right))

    def get_operators(self):
        ops = [
            Add(), Sub(),
            Mul(), Div(), Pow(),
            BAnd(), BOr(), # Xor(),
            Sin(), Cos(), Tan(),
            Bin(),
        ]
        return ops

    def mutate_op(self):
        index = rand_int(len(self.operators))
        self.operator = self.operators[index]

    def collapse(self):
        if isinstance(self.left, MathOp):
            self.left.collapse()

        if isinstance(self.right, MathOp):
            self.right.collapse()

        if self.left.is_static():
            val = MathValue()
            val.value = self.left.evaluate(None)
            self.left = val

        if self.right.is_static():
            val = MathValue()
            val.value = self.right.evaluate(None)
            self.right = val

    def mutate(self):
        # swap
        if mutate(100):
            tmp = self.left
            self.left = self.right
            self.right = tmp

        if mutate(100):
            self.collapse()

        if mutate(15):
            if self.left.is_static():
                val = MathValue()
                val.value = self.left.evaluate(None)
                self.left = val

        if mutate(15):
            if self.right.is_static():
                val = MathValue()
                val.value = self.right.evaluate(None)
                self.right = val

        # delete
        if mutate(15):
            if isinstance(self.left, MathOp):
                grand_child = self.left.left
                self.left = grand_child

        # delete
        if mutate(15):
            if isinstance(self.left, MathOp):
                grand_child = self.left.right
                self.left = grand_child

        # delete
        if mutate(15):
            if isinstance(self.right, MathOp):
                grand_child = self.right.right
                self.right = grand_child

        # delete
        if mutate(15):
            if isinstance(self.right, MathOp):
                grand_child = self.right.left
                self.right = grand_child

        # add
        if mutate(100):
            op = MathOp()
            op.left = self.left
            self.left = op

        # add
        if mutate(100):
            op = MathOp()
            op.right = self.right
            self.right = op

        # replace
        if mutate(30):
            new_left = self.create_random_node()
            self.left = new_left

        # replace
        if mutate(30):
            new_right = self.create_random_node()
            self.right = new_right

        self.left.mutate()
        self.right.mutate()
        if mutate(50):
            self.mutate_op()

    def evaluate(self, engine):
        left = self.left.evaluate(engine)
        right = self.right.evaluate(engine)
        return self.operator.evaluate(left, right)

    def clone(self):
        clone = MathOp()
        clone.operator = self.operator
        clone.left = self.left.clone()
        clone.right = self.right.clone()
        return clone

    def is_static(self):
        return self.left.is_static() and self.right.is_static()


class MathFunction(MathLiteral):
    base_op = None

    def __init__(self):
        self.base_op = MathOp()

    def __str__(self):
        return '%s' % self.base_op

    def collapse(self):
        self.base_op.collapse()

    def mutate(self):
        # add
        if mutate(100):
            op = MathOp()
            op.left = self.base_op
            self.base_op = op

        self.base_op.mutate()

    def evaluate(self, engine):
        return self.base_op.evaluate(engine)

    def clone(self):
        clone = MathFunction()
        clone.base_op = self.base_op.clone()
        return clone

    def is_static(self):
        return self.base_op.is_static()

    def get_random_node(self):
        nodes = list()
        self.traverse_node(self.base_op, nodes)

        index = rand_int(len(nodes))
        return nodes[index]

    def traverse_node(self, op, nodes):
        nodes.append(op)

        if isinstance(op.left, MathOp):
            self.traverse_node(op.left, nodes)

        if isinstance(op.right, MathOp):
            self.traverse_node(op.right, nodes)
