import sys
from dna.literals import MathFunction
from engine import Engine


class Organism():
    root = None
    problem = None
    error = None

    def __init__(self, problem):
        self.problem = problem
        self.root = MathFunction()
        self.error = sys.float_info.max

    def __str__(self):
        return '%s' % self.root

    def collapse(self):
        self.root.collapse()

    def evaluate(self, x, y):
        engine = Engine()
        engine.set_variable('x', x)
        engine.set_variable('y', y)
        res = self.root.evaluate(engine)
        return res

    def tick(self):
        engine = Engine()

        clone = self.root.clone()
        clone.mutate()

        if str(clone) == str(self.root):
            return

        tot_new_error = 0
        tot_old_error = 0
        for case in self.problem.cases:
            engine.set_variable('x', case.x)
            engine.set_variable('y', case.y)

            new_result = clone.evaluate(engine)
            old_result = self.root.evaluate(engine)

            try:
                new_error = abs(case.result - new_result)
            except OverflowError:
                new_error = abs(case.result - sys.float_info.max)

            try:
                old_error = abs(case.result - old_result)
            except OverflowError:
                old_error = abs(case.result - sys.float_info.max)

            try:
                tot_new_error += new_error
            except OverflowError:
                tot_new_error = abs(sys.float_info.max)

            try:
                tot_old_error += old_error
            except OverflowError:
                tot_old_error = abs(sys.float_info.max)

        # good match
        if (tot_new_error < tot_old_error) or ((len(str(clone)) < len(str(self.root))) and (tot_new_error < tot_old_error+sys.float_info.epsilon)):
            self.root = clone
            self.error = tot_new_error

    def clone(self):
        clone = Organism(self.problem)
        clone.root = self.root.clone()
        return clone

    def get_random_node(self):
        return self.root.get_random_node()

    def cross_over(self, father):
        child = self.clone()
        father_dna = father.get_random_node().clone()
        mother_dna = child.get_random_node()
        mother_dna.left = father_dna.left
        mother_dna.right = father_dna.right

        return child
