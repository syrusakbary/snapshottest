from __future__ import unicode_literals

import pytest
from snapshottest.module import SnapshotModule
from tests.helpers import GenericSnapshotTest, assert_snapshot_test_failed, assert_snapshot_test_succeeded


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
