from difflib import Differ
from termcolor import colored

from .formatter import Formatter


def format_line(line):
    line = line.rstrip('\n')
    if line.startswith('-'):
        return colored(line, 'red', attrs=['bold'])
    elif line.startswith('+'):
        return colored(line, 'green', attrs=['bold'])

    return colored(line, 'grey')


class PrettyDiff(object):
    def __init__(self, obj, snapshottest):
        self.obj = obj
        self.pretty = Formatter()
        self.differ = Differ()
        self.snapshottest = snapshottest

    def __eq__(self, other):
        return isinstance(other, PrettyDiff) and self.obj == other.obj

    def __repr__(self):
        return repr(self.obj)

    def get_diff(self, other):
        text1 = self.pretty(self.obj).splitlines(1)
        text2 = self.pretty(other).splitlines(1)

        lines = list(self.differ.compare(text1, text2))
        return [
            format_line(line) for line in lines
        ]
