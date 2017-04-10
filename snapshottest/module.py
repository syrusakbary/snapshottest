import os
import imp
from collections import defaultdict
import logging

from .snapshot import Snapshot
from .formatter import Formatter
# from .error import SnapshotError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SnapshotModule(object):
    _snapshot_modules = {}
    _snapshots = None

    def __init__(self, module, filepath):
        self.module = module
        self.filepath = filepath
        self.imports = defaultdict(set)
        self.imports['snapshottest'].add('Snapshot')

    def load_snapshots(self):
        try:
            source = imp.load_source(self.module, self.filepath)
            assert isinstance(source.snapshots, Snapshot)
            return source.snapshots
        except:
            return Snapshot()

    @property
    def snapshots(self):
        if not self._snapshots:
            self._snapshots = self.load_snapshots()
        return self._snapshots

    def __getitem__(self, key):
        return self.snapshots.get(key, None)

    def __setitem__(self, key, value):
        self.snapshots[key] = value

    def save(self):
        snapshot_dir = os.path.dirname(self.filepath)

        # Create the snapshot dir in case doesn't exist
        try:
            os.makedirs(snapshot_dir, 0o0700)
        except (IOError, OSError):
            pass

        # Create __init__.py in case doesn't exist
        open(os.path.join(snapshot_dir, '__init__.py'), 'a').close()

        pretty = Formatter(self.imports)

        with open(self.filepath, 'w') as snapshot_file:
            snapshots_declarations = []
            for key, value in self.snapshots.items():
                snapshots_declarations.append('''snapshots['{}'] = {}'''.format(key, pretty(value)))

            imports = '\n'.join([
                'from {} import {}'.format(module, ', '.join(module_imports))
                for module, module_imports in self.imports.items()
            ])
            snapshot_file.write('''# -*- coding: utf-8 -*-

# snapshottest: v1
# https://pypi.python.org/pypi/snapshottest

from __future__ import unicode_literals

{}


snapshots = Snapshot()

{}
'''.format(imports, '\n\n'.join(snapshots_declarations)))

    @classmethod
    def get_module_for_testpath(cls, test_filepath):
        if test_filepath not in cls._snapshot_modules:
            dirname = os.path.dirname(test_filepath)
            snapshot_dir = os.path.join(dirname, "snapshots")

            snapshot_basename = 'snap_{}'.format(os.path.basename(test_filepath))
            snapshot_filename = os.path.join(snapshot_dir, snapshot_basename)
            snapshot_module = '{}'.format(os.path.splitext(snapshot_basename)[0])

            cls._snapshot_modules[test_filepath] = SnapshotModule(snapshot_module, snapshot_filename)

        return cls._snapshot_modules[test_filepath]


class SnapshotTest(object):
    _current_tester = None
    update = False

    def __init__(self):
        self.curr_snapshot = 1

    @property
    def module(self):
        raise NotImplementedError("module property needs to be implemented")

    @property
    def update(self):
        return False

    @property
    def test_name(self):
        raise NotImplementedError("test_name property needs to be implemented")

    def __enter__(self):
        SnapshotTest._current_tester = self
        return self

    def __exit__(self, type, value, tb):
        self.save_changes()
        SnapshotTest._current_tester = None

    def store(self, data):
        self.module[self.test_name] = data
        self.curr_snapshot += 1

    def assert_equals(self, value, snapshot):
        # if value != snapshot:
        #     logger.error('OH!')
        assert value == snapshot

    def assert_match(self, value):
        prev_snapshot = not self.update and self.module[self.test_name]
        if prev_snapshot:
            self.assert_equals(value, prev_snapshot)

        self.store(value)

    def save_changes(self):
        self.module.save()


def assert_match_snapshot(value):
    if not SnapshotTest._current_tester:
        raise Exception("You need to use assert_match_snapshot in the SnapshotTest context.")

    SnapshotTest._current_tester.assert_match(value)
