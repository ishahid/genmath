from abc import ABCMeta, abstractmethod


class IEngine(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_variable(self, name):
        pass

    @abstractmethod
    def set_variable(self, name, value):
        pass


class Engine(IEngine):
    variables = None

    def __init__(self):
        self.variables = dict()

    def get_variable(self, name):
        return self.variables[name]

    def set_variable(self, name, value):
        self.variables[name] = value
