import math
from collections import defaultdict

from .sorted_dict import SortedDict
from .generic_repr import GenericRepr


class BaseFormatter(object):
    def can_format(self, value):
        raise NotImplementedError()

    def format(self, value, indent, formatter):
        raise NotImplementedError()

    def get_imports(self):
        return ()

    def assert_value_matches_snapshot(
        self, test, test_value, snapshot_value, formatter
    ):
        test.assert_equals(formatter.normalize(test_value), snapshot_value)

    def store(self, test, value):
        return value

    def normalize(self, value, formatter):
        return value


class TypeFormatter(BaseFormatter):
    def __init__(self, types, format_func):
        self.types = types
        self.format_func = format_func

    def can_format(self, value):
        return isinstance(value, self.types)

    def format(self, value, indent, formatter):
        return self.format_func(value, indent, formatter)


class CollectionFormatter(TypeFormatter):
    def normalize(self, value, formatter):
        iterator = iter(value.items()) if isinstance(value, dict) else iter(value)
        # https://github.com/syrusakbary/snapshottest/issues/115
        # Normally we shouldn't need to turn this into a list, but some iterable
        # constructors need a list not an iterator (e.g. unittest.mock.call).
        return value.__class__([formatter.normalize(item) for item in iterator])


class DefaultDictFormatter(TypeFormatter):
    def normalize(self, value, formatter):
        return defaultdict(
            value.default_factory, (formatter.normalize(item) for item in value.items())
        )


def trepr(s):
    text = "\n".join([repr(line).lstrip("u")[1:-1] for line in s.split("\n")])
    quotes, dquotes = "'''", '"""'
    if quotes in text:
        if dquotes in text:
            text = text.replace(quotes, "\\'\\'\\'")
        else:
            quotes = dquotes
    return "%s%s%s" % (quotes, text, quotes)


def format_none(value, indent, formatter):
    return "None"


def format_str(value, indent, formatter):
    if "\n" in value:
        # Is a multiline string, so we use '''{}''' for the repr
        return trepr(value)

    # Snapshots are saved with `from __future__ import unicode_literals`,
    # so the `u'...'` repr is unnecessary, even on Python 2
    return repr(value).lstrip("u")


def format_float(value, indent, formatter):
    if math.isinf(value) or math.isnan(value):
        return 'float("%s")' % repr(value)
    return repr(value)


def format_std_type(value, indent, formatter):
    return repr(value)


def format_dict(value, indent, formatter):
    value = SortedDict(value)
    items = [
        formatter.lfchar
        + formatter.htchar * (indent + 1)
        + formatter.format(key, indent)
        + ": "
        + formatter.format(value[key], indent + 1)
        for key in value
    ]
    return "{%s}" % (",".join(items) + formatter.lfchar + formatter.htchar * indent)


def format_list(value, indent, formatter):
    return "[%s]" % format_sequence(value, indent, formatter)


def format_sequence(value, indent, formatter):
    items = [
        formatter.lfchar
        + formatter.htchar * (indent + 1)
        + formatter.format(item, indent + 1)
        for item in value
    ]
    return ",".join(items) + formatter.lfchar + formatter.htchar * indent


def format_tuple(value, indent, formatter):
    return "(%s%s" % (
        format_sequence(value, indent, formatter),
        ",)" if len(value) == 1 else ")",
    )


def format_set(value, indent, formatter):
    return "set([%s])" % format_sequence(value, indent, formatter)


def format_frozenset(value, indent, formatter):
    return "frozenset([%s])" % format_sequence(value, indent, formatter)


class GenericFormatter(BaseFormatter):
    def can_format(self, value):
        return True

    def store(self, test, value):
        return GenericRepr.from_value(value)

    def normalize(self, value, formatter):
        return GenericRepr.from_value(value)

    def format(self, value, indent, formatter):
        if not isinstance(value, GenericRepr):
            value = GenericRepr.from_value(value)
        return repr(value)

    def get_imports(self):
        return [("snapshottest", "GenericRepr")]

    def assert_value_matches_snapshot(
        self, test, test_value, snapshot_value, formatter
    ):
        test_value = GenericRepr.from_value(test_value)
        # Assert equality between the representations to provide a nice textual diff.
        test.assert_equals(test_value.representation, snapshot_value.representation)


def default_formatters():
    return [
        TypeFormatter(type(None), format_none),
        DefaultDictFormatter(defaultdict, format_dict),
        CollectionFormatter(dict, format_dict),
        CollectionFormatter(tuple, format_tuple),
        CollectionFormatter(list, format_list),
        CollectionFormatter(set, format_set),
        CollectionFormatter(frozenset, format_frozenset),
        TypeFormatter((str,), format_str),
        TypeFormatter((float,), format_float),
        TypeFormatter((int, complex, bool, bytes), format_std_type),
        GenericFormatter(),
    ]
