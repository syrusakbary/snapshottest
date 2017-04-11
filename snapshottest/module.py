import os
import imp
from collections import defaultdict
import logging

from .snapshot import Snapshot
from .formatter import Formatter
from .diff import PrettyDiff
# from .error import SnapshotError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SnapshotModule(object):
    _snapshot_modules = {}

    def __init__(self, module, filepath):
        self._original_snapshot = None
        self._snapshots = None
        self.module = module
        self.filepath = filepath
        self.imports = defaultdict(set)
        self.visited_snapshots = set()
        self.new_snapshots = set()
        self.failed_snapshots = set()
        self.imports['snapshottest'].add('Snapshot')

    def load_snapshots(self):
        try:
            source = imp.load_source(self.module, self.filepath)
            assert isinstance(source.snapshots, Snapshot)
            return source.snapshots
        except:
            return Snapshot()

    def visit(self, snapshot_name):
        self.visited_snapshots.add(snapshot_name)

    def delete_unvisited(self):
        for unvisited in self.unvisited_snapshots:
            del self.snapshots[unvisited]

    @property
    def unvisited_snapshots(self):
        return set(self.snapshots.keys()) - self.visited_snapshots

    @classmethod
    def total_unvisited_snapshots(cls):
        unvisited_snapshots = 0
        unvisited_modules = 0
        for module in cls.get_modules():
            l = len(module.unvisited_snapshots)
            unvisited_snapshots += l
            unvisited_modules += min(l, 1)

        return unvisited_snapshots, unvisited_modules

    @classmethod
    def get_modules(cls):
        return SnapshotModule._snapshot_modules.values()

    @classmethod
    def stats_for_module(cls, getter):
        count_snapshots = 0
        count_modules = 0
        for module in SnapshotModule._snapshot_modules.values():
            l = getter(module)
            count_snapshots += l
            count_modules += min(l, 1)

        return count_snapshots, count_modules

    @classmethod
    def stats_unvisited_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.unvisited_snapshots))

    @classmethod
    def stats_visited_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.visited_snapshots))

    @classmethod
    def stats_new_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.new_snapshots))

    @classmethod
    def stats_failed_snapshots(cls):
        return cls.stats_for_module(lambda module: len(module.failed_snapshots))

    @classmethod
    def stats_successful_snapshots(cls):
        stats_visited = cls.stats_visited_snapshots()
        stats_failed = cls.stats_failed_snapshots()
        return stats_visited[0] - stats_failed[0]

    @classmethod
    def has_snapshots(cls):
        return cls.stats_visited_snapshots()[0] > 0

    @property
    def original_snapshot(self):
        if not self._original_snapshot:
            self._original_snapshot = self.load_snapshots()
        return self._original_snapshot

    @property
    def snapshots(self):
        if not self._snapshots:
            self._snapshots = Snapshot(self.original_snapshot)
        return self._snapshots

    def __getitem__(self, key):
        return self.snapshots.get(key, None)

    def __setitem__(self, key, value):
        if key not in self.snapshots:
            # It's a new test
            self.new_snapshots.add(key)
        self.snapshots[key] = value

    def mark_failed(self, key):
        return self.failed_snapshots.add(key)

    def save(self):
        if self.original_snapshot == self.snapshots:
            # If there are no changes, we do nothing
            return

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
# snapshottest: v1 - https://goo.gl/zC4yUc
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

            snapshot_basename = 'snap_{}.py'.format(os.path.splitext(os.path.basename(test_filepath))[0])
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

    def visit(self):
        self.module.visit(self.test_name)

    def fail(self):
        self.module.mark_failed(self.test_name)

    def store(self, data):
        self.module[self.test_name] = data
        self.curr_snapshot += 1

    def assert_equals(self, value, snapshot):
        assert value == snapshot

    def assert_match(self, value):
        self.visit()
        prev_snapshot = not self.update and self.module[self.test_name]
        if prev_snapshot:
            try:
                self.assert_equals(
                    PrettyDiff(value, self),
                    PrettyDiff(prev_snapshot, self)
                )
            except:
                self.fail()
                raise

        self.store(value)

    def save_changes(self):
        self.module.save()


def assert_match_snapshot(value):
    if not SnapshotTest._current_tester:
        raise Exception("You need to use assert_match_snapshot in the SnapshotTest context.")

    SnapshotTest._current_tester.assert_match(value)
