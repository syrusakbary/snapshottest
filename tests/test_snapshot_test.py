import pytest
from collections import OrderedDict
from time import time
from snapshottest.module import SnapshotModule, SnapshotTest


class GenericSnapshotTest(SnapshotTest):
    """A concrete SnapshotTest implementation for no particular testing framework"""

    def __init__(self, snapshot_module, update=False, current_test_id=None):
        self._generic_options = {
            "snapshot_module": snapshot_module,
            "update": update,
            "current_test_id": current_test_id or "test_mocked",
        }
        super(GenericSnapshotTest, self).__init__()

    @property
    def module(self):
        return self._generic_options["snapshot_module"]

    @property
    def update(self):
        return self._generic_options["update"]

    @property
    def test_name(self):
        return "{} {}".format(
            self._generic_options["current_test_id"], self.curr_snapshot
        )

    def reinitialize(self):
        """Reset internal state, as though starting a new test run"""
        super(GenericSnapshotTest, self).__init__()


def assert_snapshot_test_ran(snapshot_test, test_name=None):
    test_name = test_name or snapshot_test.test_name
    assert test_name in snapshot_test.module.visited_snapshots


def assert_snapshot_test_succeeded(snapshot_test, test_name=None):
    test_name = test_name or snapshot_test.test_name
    assert_snapshot_test_ran(snapshot_test, test_name)
    assert test_name not in snapshot_test.module.failed_snapshots


def assert_snapshot_test_failed(snapshot_test, test_name=None):
    test_name = test_name or snapshot_test.test_name
    assert_snapshot_test_ran(snapshot_test, test_name)
    assert test_name in snapshot_test.module.failed_snapshots


@pytest.fixture(name="snapshot_test")
def fixture_snapshot_test(tmpdir):
    filepath = tmpdir.join("snap_mocked.py")
    module = SnapshotModule("tests.snapshots.snap_mocked", str(filepath))
    return GenericSnapshotTest(module)


SNAPSHOTABLE_VALUES = [
    "abc",
    b"abc",
    123,
    123.456,
    {"a": 1, "b": 2, "c": 3},  # dict
    ["a", "b", "c"],  # list
    {"a", "b", "c"},  # set
    ("a", "b", "c"),  # tuple
    ("a",),  # tuple only have one element
    # Falsy values:
    None,
    False,
    "",
    b"",
    dict(),
    list(),
    set(),
    tuple(),
    0,
    0.0,
    # dict subclasses:
    # (Make sure snapshots don't just coerce to dict for comparison.)
    OrderedDict([("a", 1), ("b", 2), ("c", 3)]),  # same items as earlier dict
    OrderedDict([("c", 3), ("b", 2), ("a", 1)]),  # same items, different order
]


@pytest.mark.parametrize("value", SNAPSHOTABLE_VALUES, ids=repr)
def test_snapshot_matches_itself(snapshot_test, value):
    # first run stores the value as the snapshot
    snapshot_test.assert_match(value)
    assert_snapshot_test_succeeded(snapshot_test)

    # second run should compare stored snapshot and also succeed
    snapshot_test.reinitialize()
    snapshot_test.assert_match(value)
    assert_snapshot_test_succeeded(snapshot_test)


@pytest.mark.parametrize(
    "value, other_value",
    [
        pytest.param(
            value,
            other_value,
            id="snapshot {!r} shouldn't match {!r}".format(value, other_value),
        )
        for value in SNAPSHOTABLE_VALUES
        for other_value in SNAPSHOTABLE_VALUES
        if other_value != value
    ],
)
def test_snapshot_does_not_match_other_values(snapshot_test, value, other_value):
    # first run stores the value as the snapshot
    snapshot_test.assert_match(value)
    assert_snapshot_test_succeeded(snapshot_test)

    # second run tries to match other_value, should fail
    snapshot_test.reinitialize()
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(other_value)
    assert_snapshot_test_failed(snapshot_test)


SNAPSHOTABLE_VALUES_WITH_IGNORE = [
    {
        "data": {"dict1": {"dict2": {"dict3": {"id": time(), "other": "value"}}}},
        "ignore_keys": ["dict1.dict2.dict3.id"],
    },
    {
        "data": [
            {
                "A": {
                    "id": time(),
                    "B": 1,
                    "C": 2,
                    "D": [0, 1, {"A": 1}],
                }
            },
            {
                "A": {
                    "id": time(),
                    "B": 2,
                    "C": 3,
                    "D": [0, 1, {"id": time()}],
                }
            },
        ],
        "ignore_keys": ["[.].A.id", "[1].A.C[.].id"],
    },
    {
        "data": {
            "A": {
                "id": [0, 1, 2, 3, time()],
                "A": 1,
                "B": 2,
                "C": [
                    {"id": time()},
                    {"id": time(), "A": 0},
                    {"id": time()},
                ],
            }
        },
        "ignore_keys": ["A.C[.].id", "A.id[4]"],
    },
    {
        "data": {
            "A": {
                "A": {
                    "id": time(),
                    "A": 1,
                    "B": 2,
                    "C": 3,
                    "D": [
                        {"id": [0, time()]},
                        {"id": {"A": [time()]}, "B": 0},
                        {"id": time()},
                    ],
                }
            }
        },
        "ignore_keys": ["A.A.id", "A.A.D.id[1]", "A.A.D.id.A[0"],
    },
]


@pytest.mark.parametrize("values", SNAPSHOTABLE_VALUES_WITH_IGNORE, ids=repr)
def test_snapshot_with_ignore(snapshot_test, values):
    data = values["data"]
    ignore_keys = values["ignore_keys"]
    snapshot_test.assert_match_with_ignore(data, ignore_keys)

    snapshot_test.reinitialize()
    snapshot_test.assert_match_with_ignore(data, ignore_keys)
    assert_snapshot_test_succeeded(snapshot_test)
