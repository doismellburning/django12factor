import os


class EnvironmentVariableLoader(object):
    def __init__(self, name, **kwargs):
        self.name = name

    def load_value(self):
        return os.getenv(self.name)


EVL = EnvironmentVariableLoader
