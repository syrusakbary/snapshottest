from unittest.mock import Mock

import pytest

from snapshottest.module import SnapshotModule, SnapshotTest
from tests.helpers import GenericSnapshotTest, assert_snapshot_test_succeeded, assert_snapshot_test_failed

@pytest.fixture()
def snapshot_module(tmpdir):
    filepath = tmpdir.join("snap_mocked.py")
    module = SnapshotModule("tests.snapshots.snap_mocked", str(filepath))
    return module

@pytest.fixture(name="snapshot_test")
def fixture_snapshot_test(snapshot_module):
    return GenericSnapshotTest(snapshot_module)

# Behavior common for number of stragegies

@pytest.mark.parametrize('record_mode', ['new_interactions', 'once', 'all'])
def test_store_new_snapshot(snapshot_module, snapshot_test, record_mode):
    snapshot_test._generic_options["record_mode"] = record_mode
    snapshot_test.current_test_has_some_snapshots = Mock(return_value=False)
    value = 1
    # When: first run stores the value as the snapshot
    snapshot_test.assert_match(value)
    # Then
    assert_snapshot_test_succeeded(snapshot_test)
    # And
    assert snapshot_module[snapshot_test.test_name] == value

@pytest.mark.parametrize('record_mode', ['none', 'new_interactions', 'once'])
def test_match_fail_on_existing_snapshot(
        snapshot_module, snapshot_test, record_mode):
    snapshot_test._generic_options["record_mode"] = record_mode
    old_value = 1
    new_value = 2
    # Given: old_value already stored for `fixed` snapshot of test_mocked test
    snapshot_test.curr_snapshot = 'fixed'
    snapshot_test.store(old_value)
    # When: we try to assert a new value for `fixed` snapshot
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(new_value, name='fixed')
    # Then
    assert_snapshot_test_failed(snapshot_test)

    
# Behavior specific for strategies

def test_match_works_on_existing_snapshot_for_all_record_mode(
        snapshot_module, snapshot_test):
    snapshot_test._generic_options["record_mode"] = 'all'
    old_value = {'a': 1}
    new_value = {'a': 2}
    snapshot_test.assert_match(old_value, name='fixed')
    # When:
    snapshot_test.assert_match(new_value, name='fixed')
    # Then
    assert_snapshot_test_succeeded(snapshot_test)

def test_match_fails_on_new_snapshot_for_none_record_mode(
        snapshot_module, snapshot_test):
    # Given: snapshot test has none starategy
    snapshot_test._generic_options["record_mode"] = 'none'
    value = 1
    # When: first run stores the value as the snapshot
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(value)
    # Then
    assert_snapshot_test_failed(snapshot_test)

def test_match_fails_on_new_snapshot_in_recorded_test_for_once_record_mode(
        snapshot_module, snapshot_test):
    # Given: snapshot test has once starategy
    snapshot_test._generic_options["record_mode"] = 'once'
    value = 1
    # Given: snashot test is mocked to say test has some snapshots
    snapshot_test.current_test_has_some_snapshots = Mock(return_value=True)
    # When: first run stores the value as the snapshot
    with pytest.raises(AssertionError):
        snapshot_test.assert_match(value)
    # Then
    assert_snapshot_test_failed(snapshot_test)

# 