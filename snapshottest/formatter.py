import six
import datetime
from .sorted_dict import SortedDict
from .generic_repr import GenericRepr


def trepr(s):
    text = '\n'.join([repr(line)[1:-1] for line in s.split('\n')])
    quotes, dquotes = "'''", '"""'
    if quotes in text:
        if dquotes in text:
            text = text.replace(quotes, "\\'\\'\\'")
        else:
            quotes = dquotes
    return "%s%s%s" % (quotes, text, quotes)


class Formatter(object):
    def __init__(self, imports=None):
        self.types = {}
        self.htchar = ' ' * 4
        self.lfchar = '\n'
        self.indent = 0
        self.imports = imports

    def set_formater(self, obj, callback):
        self.types[obj] = callback

    def __call__(self, value, **args):
        return self.format(value, self.indent)

    def format(self, value, indent):
        from .diff import PrettyDiff
        if value is None:
            return 'None'
        if isinstance(value, PrettyDiff):
            return self.format(value.obj, indent)
        if isinstance(value, dict):
            return self.format_dict(value, indent)
        elif isinstance(value, tuple):
            return self.format_tuple(value, indent)
        elif isinstance(value, list):
            return self.format_list(value, indent)
        elif isinstance(value, six.string_types):
            return self.format_str(value, indent)
        elif isinstance(value, (int, float, complex, bool, bytes, set, frozenset, GenericRepr)):
            return self.format_std_type(value, indent)
        elif isinstance(value, datetime.datetime):
            return self.format_str(str(value), indent)

        return self.format_object(value, indent)

    def format_str(self, value, indent):
        if '\n' in value:
            # Is a multiline string, so we use '''{}''' for the repr
            return trepr(value)

        return repr(value)

    def format_std_type(self, value, indent):
        return repr(value)

    def format_object(self, value, indent):
        if self.imports:
            self.imports['snapshottest'].add('GenericRepr')
        return repr(GenericRepr(value))

    def format_dict(self, value, indent):
        value = SortedDict(**value)
        items = [
            self.lfchar + self.htchar * (indent + 1) + self.format(key, indent) + ': ' +
            self.format(value[key], indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + self.lfchar + self.htchar * indent)

    def format_list(self, value, indent):
        items = [
            self.lfchar + self.htchar * (indent + 1) + self.format(item, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + self.lfchar + self.htchar * indent)

    def format_tuple(self, value, indent):
        items = [
            self.lfchar + self.htchar * (indent + 1) + self.format(item, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + self.lfchar + self.htchar * indent)
