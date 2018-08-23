# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import six
from datetime import date
from collections import defaultdict

from snapshottest.formatter import Formatter


@pytest.mark.parametrize("text_value, expected", [
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
    ("three\n'''quotes", "\"\"\"three\n'''quotes\"\"\""),
    ("so many\"\"\"\n'''quotes", "'''so many\"\"\"\n\\'\\'\\'quotes'''"),
    # Generic representations
    (date(2018, 1, 1), "GenericRepr('datetime.date(2018, 1, 1)')"),
])
def test_text_formatting(text_value, expected):
    formatter = Formatter(defaultdict(set))
    formatted = formatter(text_value)
    assert formatted == expected

    if six.PY2:
        # Also check that Python 2 str value formats the same as the unicode value.
        # (If a test case raises UnicodeEncodeError in here, it should be moved to
        # the non_ascii verson of this test, below.)
        py2_str_value = text_value.encode("ASCII")
        py2_str_formatted = formatter(py2_str_value)
        assert py2_str_formatted == expected


# When unicode snapshots are saved in Python 2, there's no easy way to generate
# a clean unicode_literals repr that doesn't use escape sequences. But the
# resulting snapshots are still valid on Python 3 (and vice versa).
@pytest.mark.parametrize("text_value, expected_py3, expected_py2", [
    ("encodage précis", "'encodage précis'", "'encodage pr\\xe9cis'"),
    ("精确的编码", "'精确的编码'", "'\\u7cbe\\u786e\\u7684\\u7f16\\u7801'"),
    # backslash [unicode repr can't just be `"u'{}'".format(value)`]
    ("omvänt\\snedstreck", "'omvänt\\\\snedstreck'", "'omv\\xe4nt\\\\snedstreck'"),
    # multiline
    ("ett\ntvå\n", "'''ett\ntvå\n'''", "'''ett\ntv\\xe5\n'''"),
])
def test_non_ascii_text_formatting(text_value, expected_py3, expected_py2):
    expected = expected_py2 if six.PY2 else expected_py3
    formatter = Formatter(defaultdict(set))
    formatted = formatter(text_value)
    assert formatted == expected
