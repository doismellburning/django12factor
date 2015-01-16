import os


identity = lambda x: x


class EnvironmentVariableLoader(object):
    def __init__(self, name, default=None, parser=identity):
        self.name = name
        self.default = default
        self.parser = parser

    def load_value(self):
        if self.name in os.environ:
            return self.parser(os.environ[self.name])
        else:
            return self.default


EVL = EnvironmentVariableLoader
