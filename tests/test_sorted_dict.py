# -*- coding: utf-8 -*-
import enum

import pytest

from snapshottest.sorted_dict import SortedDict


@pytest.mark.parametrize(
    "key, value",
    [
        ("key1", "value"),
        ("key2", 42),
        ("key3", ["value"]),
        ("key4", [["value"]]),
        ("key5", {"key": "value"}),
        ("key6", [{"key": "value"}]),
        ("key7", {"key": ["value"]}),
        ("key8", [{"key": ["value"]}]),
    ],
)
def test_sorted_dict(key, value):
    dic = dict([(key, value)])
    assert SortedDict(dic)[key] == value


def test_sorted_dict_string_key():
    value = ("key", "value")
    dic = dict([value])
    assert SortedDict(dic)[value[0]] == value[1]


def test_sorted_dict_int_key():
    value = (0, "value")
    dic = dict([value])
    assert SortedDict(dic)[value[0]] == value[1]


def test_sorted_dict_intenum():
    class Fruit(enum.IntEnum):
        APPLE = 1
        ORANGE = 2

    dic = {Fruit.APPLE: 100, Fruit.ORANGE: 400}
    assert SortedDict(dic)[Fruit.APPLE] == dic[Fruit.APPLE]
    assert SortedDict(dic)[Fruit.ORANGE] == dic[Fruit.ORANGE]


def test_sorted_dict_enum():
    class Fruit(enum.Enum):
        APPLE = 1
        ORANGE = 2

    dic = {Fruit.APPLE: 100, Fruit.ORANGE: 400}
    assert SortedDict(dic)[Fruit.APPLE] == dic[Fruit.APPLE]
    assert SortedDict(dic)[Fruit.ORANGE] == dic[Fruit.ORANGE]


def test_sorted_dict_enum_value():
    class Fruit(enum.Enum):
        APPLE = 1
        ORANGE = 2

    value = ("fruit", Fruit)
    dic = dict([value])
    assert SortedDict(dic)[value[0]] == value[1]


def test_sorted_dict_enum_key():
    class Fruit(enum.Enum):
        APPLE = 1
        ORANGE = 2

    value = (Fruit, "fruit")
    dic = dict([value])
    assert SortedDict(dic)[value[0]] == value[1]
