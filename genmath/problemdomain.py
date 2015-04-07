class Case:
    x = 0
    y = 0
    result = 0

    def __init__(self, x, y, result):
        self.x = x
        self.y = y
        self.result = result


class Problem:
    cases = None

    def __init__(self):
        self.cases = list()
