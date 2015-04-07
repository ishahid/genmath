#!/usr/bin/env python

"""
Python implementation of Roger Alsing's GenMath.
http://rogeralsing.com/2008/02/07/genetic-programming-math/
"""

import sys, math
from genmath.problemdomain import Problem, Case
from genmath.organism import Organism
from genmath.tools import rand_int, print_out, console_colours


if __name__ == "__main__":
    generations = 0
    problem = Problem()

    # f(x, y) = x + y
    problem.cases.append(Case(0, 1, 1))
    problem.cases.append(Case(1, 1, 2))
    problem.cases.append(Case(1, 2, 3))
    problem.cases.append(Case(2, 3, 5))
    problem.cases.append(Case(3, 5, 8))

    # f(x, y) = x ** y
    # problem.cases.append(Case(1, 2, 1))
    # problem.cases.append(Case(2, 3, 8))
    # problem.cases.append(Case(3, 4, 81))
    # problem.cases.append(Case(4, 5, 1024))

    # f(x, y) = x * (x + y)
    # problem.cases.append(Case(2, 3, 10))
    # problem.cases.append(Case(7, 2, 63))
    # problem.cases.append(Case(6, 5, 66))
    # problem.cases.append(Case(8, 4, 96))

    # f(x, y) = ?
    # problem.cases.append(Case(47, 3, 533))
    # problem.cases.append(Case(30, 5, 365))
    # problem.cases.append(Case(15, 7.5, 217.5))

    # f(x, y) = (pi * x) + y
    # problem.cases.append(Case(2, 1, math.pi * 2 + 1))
    # problem.cases.append(Case(5, 2, math.pi * 5 + 2))
    # problem.cases.append(Case(9, 3, math.pi * 9 + 3))
    # problem.cases.append(Case(7325, 4, math.pi * 7325 + 4))

    # f(x, y) = (((x + x) * y) - 1.7) - (x * 0.7)
    # problem.cases.append(Case(1, 1, 0.3 - 1 * 0.7))
    # problem.cases.append(Case(1, 2, 2.3 - 1 * 0.7))
    # problem.cases.append(Case(2, 2, 6.3 - 2 * 0.7))
    # problem.cases.append(Case(3, 1, 4.3 - 3 * 0.7))
    # problem.cases.append(Case(10, 10, 198.3 - 10 * 0.7))

    # f(x, y) = (x & y) + 1
    # problem.cases.append(Case(1, 255, 1 + 1))
    # problem.cases.append(Case(2, 255, 2 + 1))
    # problem.cases.append(Case(1, 0, 0 + 1))
    # problem.cases.append(Case(1, 2, 0 + 1))
    # problem.cases.append(Case(16, 16, 16 + 1))
    # problem.cases.append(Case(16, 255, 16 + 1))
    # problem.cases.append(Case(17, 255, 17 + 1))

    # f(x, y) = ???
    # problem.cases.append(Case(1, 5, 55))
    # problem.cases.append(Case(3, 6, 63))
    # problem.cases.append(Case(7, 7, 78))
    # problem.cases.append(Case(13, 5, 99))

    # f(x, y) = bin(x) + 5
    # for i in range(0, 8):
    #     tmp = '%s' % bin(i)[2:]
    #     res = int(tmp) + 5
    #     problem.cases.append(Case(i, 0, res))

    # f(x, y) = (sin(x) * 100) + y
    # for i in range(0, 4):
    #     problem.cases.append(Case(i, 0, math.sin(i) * 100))

    # create an initial population
    organisms = list()
    for i in range(0, 50):
        organism = Organism(problem)
        organisms.append(organism)

    done = False
    best_error = sys.float_info.max
    previous_error = best_error
    min_error = 0.000000000001
    worst_error = sys.float_info.min
    best_organism = None
    worst_organism = None

    while not done:
        generations += 1
        avg_error = 0

        for organism in organisms:
            organism.tick()

            if organism.error < best_error:
                best_error = organism.error
                best_organism = organism

            if organism.error > worst_error:
                worst_error = organism.error
                worst_organism = organism

            if organism.error < min_error:
                done = True
                break

        if rand_int(10) == 1:
            organisms.remove(worst_organism)
            clone = best_organism.clone()
            organisms.append(clone)

        elif rand_int(30) == 1:
            organisms.remove(worst_organism)
            index = rand_int(len(organisms))
            clone = organisms[index].clone()
            organisms.append(clone)

        elif rand_int(100) == 1:
            organisms.remove(worst_organism)

            index = rand_int(len(organisms))
            mother = best_organism
            father = organisms[index]
            child = mother.cross_over(father)

            organisms.append(child)

        worst_organism = None
        worst_error = sys.float_info.min

        if best_error != previous_error:
            if best_organism is not None:
                colour = console_colours['white']

                if best_error / previous_error < 0.94:
                    colour = console_colours['red']

                elif best_error / previous_error < 0.96:
                    colour = console_colours['yellow']

                elif best_error / previous_error < 0.98:
                    colour = console_colours['cyan']

                print_out('Error Level: %s, Organism: %s' % (best_error, best_organism), colour=colour)
                colour = console_colours['white']

            previous_error = best_error

    print_out('Generations: %s' % generations)
    print_out('')
    print_out('Solved...')
    print_out('%s' % best_organism)
    print_out('')
    print_out('Proof...')

    for case in problem.cases:
        res = best_organism.evaluate(case.x, case.y)
        print_out('x = %s, y = %s, goal = %s, actual = %s' % (case.x, case.y, case.result, res))

    # optional optimization to get shorter formula
    if True:
        print_out('')
        print_out('Trying to optimize...')
        old_length = len('%s' % best_organism)
        best_organism.collapse()
        while True:
            best_organism.tick()

            l = len('%s' % best_organism)
            if l < old_length:
                print_out('Better Organism: %s' % best_organism)
                old_length = l
