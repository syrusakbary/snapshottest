from __future__ import unicode_literals

import time

import pytest

from snapshottest.module import SnapshotModule, SnapshotTest


class GenericSnapshotTest(SnapshotTest):
    """A concrete SnapshotTest implementation for no particular testing framework"""

    def __init__(self, snapshot_module, update=False, current_test_id=None):
        self._generic_options = {
            'snapshot_module': snapshot_module,
            'update': update,
            'current_test_id': current_test_id or "test_mocked"}
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
            self._generic_options["current_test_id"],
            self.curr_snapshot)

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
    ("a",),           # tuple only have one element

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


@pytest.mark.parametrize("value, other_value", [
    pytest.param(value, other_value,
                 id="snapshot {!r} shouldn't match {!r}".format(value, other_value))
    for value in SNAPSHOTABLE_VALUES
    for other_value in SNAPSHOTABLE_VALUES if other_value != value
])
def test_snapshot_does_not_match_other_values(snapshot_test, value, other_value):
    # first run stores the value as the snapshot
    snapshot_test.assert_match(value)
    assert_snapshot_test_succeeded(snapshot_test)

    # second run tries to match other_value, should fail
    snapshot_test.reinitialize()
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(other_value)
    assert_snapshot_test_failed(snapshot_test)


SNAPSHOTABLE_DATA_FACTORIES = {
    "dict": lambda: {"time": time.time(), "this key": "must match"},
    "nested dict": lambda: {"nested": {"time": time.time(), "this key": "must match"}},
    "dict in list": lambda: [{"time": time.time(), "this key": "must match"}],
    "dict in tuple": lambda: ({"time": time.time(), "this key": "must match"},),
    "dict in list in dict": lambda: {"list": [{"time": time.time(), "this key": "must match"}]},
    "dict in tuple in dict": lambda: {"tuple": ({"time": time.time(), "this key": "must match"},)}
}


@pytest.mark.parametrize(
    "data_factory",
    [
        pytest.param(data_factory)
        for data_factory in SNAPSHOTABLE_DATA_FACTORIES.values()
    ], ids=list(SNAPSHOTABLE_DATA_FACTORIES.keys())
)
def test_snapshot_assert_match__matches_with_diffing_ignore_keys(
    snapshot_test, data_factory
):
    data = data_factory()
    # first run stores the value as the snapshot
    snapshot_test.assert_match(data)

    # Assert with ignored keys should succeed
    data = data_factory()
    snapshot_test.reinitialize()
    snapshot_test.assert_match(data, ignore_keys=("time",))
    assert_snapshot_test_succeeded(snapshot_test)

    # Assert without ignored key should raise
    data = data_factory()
    snapshot_test.reinitialize()
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(data)


@pytest.mark.parametrize(
    "existing_snapshot, new_snapshot",
    [
        pytest.param(
            {"time": time.time(), "some_key": "some_value"},
            {"some_key": "some_value"},
            id="new_snapshot_missing_key",
        ),
        pytest.param(
            {"some_key": "some_value"},
            {"time": time.time(), "some_key": "some_value"},
            id="new_snapshot_extra_key",
        ),
    ],
)
def test_snapshot_assert_match_does_not_match_if_ignore_keys_not_present(
    snapshot_test, existing_snapshot, new_snapshot
):
    # first run stores the value as the snapshot
    snapshot_test.assert_match(existing_snapshot)

    snapshot_test.reinitialize()
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(new_snapshot, ignore_keys=("time",))
