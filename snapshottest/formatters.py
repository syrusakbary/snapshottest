import six

from .sorted_dict import SortedDict
from .generic_repr import GenericRepr


class BaseFormatter(object):
    def can_format(self, value):
        raise NotImplementedError()

    def format(self, value, indent, formatter):
        raise NotImplementedError()

    def get_imports(self):
        return ()

    def assert_value_matches_snapshot(self, test, test_value, snapshot_value):
        test.assert_equals(test_value, snapshot_value)

    def store(self, test, value):
        return value


class TypeFormatter(BaseFormatter):
    def __init__(self, types, format_func):
        self.types = types
        self.format_func = format_func

    def can_format(self, value):
        return isinstance(value, self.types)

    def format(self, value, indent, formatter):
        return self.format_func(value, indent, formatter)


def trepr(s):
    text = '\n'.join([repr(line).lstrip('u')[1:-1] for line in s.split('\n')])
    quotes, dquotes = "'''", '"""'
    if quotes in text:
        if dquotes in text:
            text = text.replace(quotes, "\\'\\'\\'")
        else:
            quotes = dquotes
    return "%s%s%s" % (quotes, text, quotes)


def format_none(value, indent, formatter):
    return 'None'


def format_str(value, indent, formatter):
    if '\n' in value:
        # Is a multiline string, so we use '''{}''' for the repr
        return trepr(value)

    # Snapshots are saved with `from __future__ import unicode_literals`,
    # so the `u'...'` repr is unnecessary, even on Python 2
    return repr(value).lstrip('u')


def format_std_type(value, indent, formatter):
    return repr(value)


def format_dict(value, indent, formatter):
    value = SortedDict(**value)
    items = [
        formatter.lfchar + formatter.htchar * (indent + 1) + formatter.format(key, indent) + ': ' +
        formatter.format(value[key], indent + 1)
        for key in value
    ]
    return '{%s}' % (','.join(items) + formatter.lfchar + formatter.htchar * indent)


def format_list(value, indent, formatter):
    items = [
        formatter.lfchar + formatter.htchar * (indent + 1) + formatter.format(item, indent + 1)
        for item in value
    ]
    return '[%s]' % (','.join(items) + formatter.lfchar + formatter.htchar * indent)


def format_tuple(value, indent, formatter):
    items = [
        formatter.lfchar + formatter.htchar * (indent + 1) + formatter.format(item, indent + 1)
        for item in value
    ]
    return '(%s,)' % (','.join(items) + formatter.lfchar + formatter.htchar * indent)


class GenericFormatter(BaseFormatter):
    def can_format(self, value):
        return True

    def store(self, formatter, value):
        return GenericRepr.from_value(value)

    def format(self, value, indent, formatter):
        # `value` will always be a GenericRepr object because that's what `store` returns.
        return repr(value)

    def get_imports(self):
        return [('snapshottest', 'GenericRepr')]

    def assert_value_matches_snapshot(self, test, test_value, snapshot_value):
        test_value = GenericRepr.from_value(test_value)
        # Assert equality between the representations to provide a nice textual diff.
        test.assert_equals(test_value.representation, snapshot_value.representation)


def default_formatters():
    return [
        TypeFormatter(type(None), format_none),
        TypeFormatter(dict, format_dict),
        TypeFormatter(tuple, format_tuple),
        TypeFormatter(list, format_list),
        TypeFormatter(six.string_types, format_str),
        TypeFormatter((int, float, complex, bool, bytes, set, frozenset), format_std_type),
        GenericFormatter()
    ]
