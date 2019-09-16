import os
import shutil
import filecmp
import functools

from .formatter import Formatter
from .formatters import BaseFormatter


class FileSnapshot(object):
    def __init__(self, path, comparison=None):
        """
        Create a file snapshot pointing to the specified `path`. In a snapshot, `path` is considered to be relative to
        the test module's "snapshots" folder. (This is done to prevent ugly path manipulations inside the snapshot
        file.)

        `comparison` can be used to provide a custom comparison function that tests that two files are identical.
        The function signature should match the default implementation:

            def compare_files_default(new_file_path: str, snapshot_file_path: str) -> bool:
                return filecmp.cmp(new_file_path, snapshot_file_path, shallow=False)

        """
        self.path = path
        if comparison is None:
            comparison = functools.partial(filecmp.cmp, shallow=False)
        self.comparison = comparison

    def __repr__(self):
        return 'FileSnapshot({})'.format(repr(self.path))

    def __eq__(self, other):
        return self.path == other.path


class FileSnapshotFormatter(BaseFormatter):
    def can_format(self, value):
        return isinstance(value, FileSnapshot)

    def store(self, test, value):
        """
        Copy the file from the test location to the snapshot location.
        If the original test file has an extension, the snapshot file will use the same extension.
        """

        file_snapshot_dir = self.get_file_snapshot_dir(test)
        if not os.path.exists(file_snapshot_dir):
            os.makedirs(file_snapshot_dir, 0o0700)
        extension = os.path.splitext(value.path)[1]
        snapshot_file = os.path.join(file_snapshot_dir, test.test_name) + extension
        shutil.copy(value.path, snapshot_file)
        relative_snapshot_filename = os.path.relpath(snapshot_file, test.module.snapshot_dir)
        return FileSnapshot(relative_snapshot_filename)

    def get_imports(self):
        return (('snapshottest.file', 'FileSnapshot'),)

    def format(self, value, indent, formatter):
        return repr(value)

    def assert_value_matches_snapshot(self, test, test_value, snapshot_value, formatter):
        snapshot_path = os.path.join(test.module.snapshot_dir, snapshot_value.path)
        comparison_function = test_value.comparison
        files_identical = comparison_function(test_value.path, snapshot_path)
        assert files_identical, "Stored file differs from test file"

    @staticmethod
    def get_file_snapshot_dir(test):
        """
        Get the directory for storing file snapshots for `test`.
        Snapshot files are stored under:
            snapshots/snap_<test_module_name>/
        Right next to where the snapshot module is stored:
            snapshots/snap_<snapshot_module_name>.py
        """
        return os.path.join(test.module.snapshot_dir, test.module.module)


Formatter.register_formatter(FileSnapshotFormatter())
