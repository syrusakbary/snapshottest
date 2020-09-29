from .formatters import default_formatters


class Formatter(object):
    formatters = default_formatters()

    def __init__(self, imports=None):
        self.htchar = " " * 4
        self.lfchar = "\n"
        self.indent = 0
        self.imports = imports

    def __call__(self, value, **args):
        return self.format(value, self.indent)

    def format(self, value, indent):
        formatter = self.get_formatter(value)
        for module, import_name in formatter.get_imports():
            self.imports[module].add(import_name)
        return formatter.format(value, indent, self)

    def normalize(self, value):
        formatter = self.get_formatter(value)
        return formatter.normalize(value, self)

    @staticmethod
    def get_formatter(value):
        for formatter in Formatter.formatters:
            if formatter.can_format(value):
                return formatter

        # This should never happen as GenericFormatter is registered by default.
        raise RuntimeError("No formatter found for value")

    @staticmethod
    def register_formatter(formatter):
        Formatter.formatters.insert(0, formatter)
