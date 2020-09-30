import pytest

from snapshottest import Snapshot
from snapshottest.module import SnapshotModule


class TestSnapshotModuleLoading(object):
    def test_load_not_yet_saved(self, tmpdir):
        filepath = tmpdir.join("snap_new.py")
        assert not filepath.check()  # file does not exist
        module = SnapshotModule("tests.snapshots.snap_new", str(filepath))
        snapshots = module.load_snapshots()
        assert isinstance(snapshots, Snapshot)

    def test_load_missing_package(self, tmpdir):
        filepath = tmpdir.join("snap_import.py")
        filepath.write_text("import missing_package\n", "utf-8")
        module = SnapshotModule("tests.snapshots.snap_import", str(filepath))
        with pytest.raises(ImportError):
            module.load_snapshots()

    def test_load_corrupted_snapshot(self, tmpdir):
        filepath = tmpdir.join("snap_error.py")
        filepath.write_text("<syntax error>\n", "utf-8")
        module = SnapshotModule("tests.snapshots.snap_error", str(filepath))
        with pytest.raises(SyntaxError):
            module.load_snapshots()
