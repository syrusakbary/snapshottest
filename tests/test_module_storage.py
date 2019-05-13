import sys, os
from contextlib import contextmanager

import pytest

from snapshottest.module import SnapshotModule

# Helpers

@contextmanager
def add_to_sys_path(path: str):
    full_path = os.path.abspath(path)
    sys.path.append(full_path)
    yield
    sys.path.pop()

# Test data

TEST_SNAPSHOT_FILE = '''
# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()
snapshots['{snapshot_name}'] = '{snapshot_value}'
'''

# Fixtures

@pytest.fixture()
def filepath(tmpdir):
    return tmpdir.join("snapshot_module.py")

@pytest.fixture()
def module(filepath):
    return SnapshotModule("tests.snapshots.snapshot_module", str(filepath))

# Tests

def test_snapshot_save_works(module, tmpdir):
    # Given: directly encodible value (formattin does not change it)
    value = {'a': 1}
    test_name = 'some test'
    # When: add value for test_name and save
    module[test_name] = value
    module.save()
    # Then: snapshot file actually contains of snapshot 
    with add_to_sys_path(str(tmpdir)):
        import snapshot_module
    assert list(snapshot_module.snapshots.keys()) == [test_name]
    assert snapshot_module.snapshots[test_name] == value

def test_snapshot_load(module, filepath):
    # Given: module associated to filled snapshot file
    test_snapshot_file = TEST_SNAPSHOT_FILE.format(
        snapshot_name='existing snapshot',
        snapshot_value='value')
    open(str(filepath), 'w').write(test_snapshot_file)
    # Then: load_snapshots() loads snapshot from file
    assert module.storage.load_snapshots()['existing snapshot'] == 'value'
    # And: module works like load_snapshots()
    assert module['existing snapshot'] == 'value'

