import sys
import random


def rand_int(chance):
    random.seed()
    return random.randrange(0, chance, 1)


def rand_double():
    random.seed()
    return random.random()


def mutate(chance):
    random.seed()
    if random.randrange(0, chance, 1) == 1:
        return True
    else:
        return False


console_colours = {
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'magenta': 5,
    'cyan': 6,
    'white': 7
}

def has_colours(stream):
    if not hasattr(stream, 'isatty'):
        return False

    if not stream.isatty():
        return False    # auto color only on TTYs

    try:
        import curses
        curses.setupterm()
        return curses.tigetnum('colors') > 2

    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)


def print_out(text, colour=console_colours['white']):
    if has_colours:
        seq = '\x1b[1;%dm' % (30 + colour) + text + '\x1b[0m\n'
    else:
        seq = '%s\n' % text

    sys.stdout.write(seq)
