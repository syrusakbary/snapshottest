# -*- coding: utf-8 -*-
import pytest
from math import isnan

from snapshottest.formatter import Formatter

import unittest.mock


@pytest.mark.parametrize(
    "text_value, expected",
    [
        # basics
        ("abc", "'abc'"),
        ("", "''"),
        ("back\\slash", "'back\\\\slash'"),
        # various embedded quotes (single line)
        ("""it has "double quotes".""", """'it has "double quotes".'"""),
        ("""it's got single quotes""", '''"it's got single quotes"'''),
        ("""it's got "both quotes".""", """'it\\'s got "both quotes".'"""),
        # multiline gets formatted as triple-quoted
        ("one\ntwo\n", "'''one\ntwo\n'''"),
        ("three\n'''quotes", '"""three\n\'\'\'quotes"""'),
        ("so many\"\"\"\n'''quotes", "'''so many\"\"\"\n\\'\\'\\'quotes'''"),
    ],
)
def test_text_formatting(text_value, expected):
    formatter = Formatter()
    formatted = formatter(text_value)
    assert formatted == expected


@pytest.mark.parametrize(
    "text_value, expected",
    [
        ("encodage précis", "'encodage précis'"),
        ("精确的编码", "'精确的编码'"),
        # backslash [unicode repr can't just be `"u'{}'".format(value)`]
        ("omvänt\\snedstreck", "'omvänt\\\\snedstreck'"),
        # multiline
        ("ett\ntvå\n", "'''ett\ntvå\n'''"),
    ],
)
def test_non_ascii_text_formatting(text_value, expected):
    formatter = Formatter()
    formatted = formatter(text_value)
    assert formatted == expected


# https://github.com/syrusakbary/snapshottest/issues/115
def test_can_normalize_unittest_mock_call_object():
    formatter = Formatter()
    print(formatter.normalize(unittest.mock.call(1, 2, 3)))


def test_can_normalize_iterator_objects():
    formatter = Formatter()
    print(formatter.normalize(x for x in range(3)))


@pytest.mark.parametrize(
    "value", [0, 12.7, True, False, None, float("-inf"), float("inf")]
)
def test_basic_formatting_parsing(value):
    formatter = Formatter()
    formatted = formatter(value)
    parsed = eval(formatted)
    assert parsed == value
    assert type(parsed) == type(value)


def test_formatting_parsing_nan():
    value = float("nan")

    formatter = Formatter()
    formatted = formatter(value)
    parsed = eval(formatted)
    assert isnan(parsed)
