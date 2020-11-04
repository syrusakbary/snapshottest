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


class TestSnapshotModuleBeforeWriteCallback(object):
    def test_callback_are_applied_to_data(self, tmpdir):
        filepath = tmpdir.join("snap_module.py")

        SnapshotModule.register_before_file_write_callback(
            lambda data: f"# a comment \n{data}"
        )
        SnapshotModule.register_before_file_write_callback(
            lambda data: f"# and another \n{data}"
        )

        module = SnapshotModule("tests.snapshots.snap_module", str(filepath))
        module["my_test"] = "result"

        module.save()

        with open(filepath) as snap_file:
            result = snap_file.read()

        assert result.startswith("# and another \n# a comment")
        assert "my_test" in result

    def test_can_clear_callback(self, tmpdir):
        filepath = tmpdir.join("snap_module.py")

        SnapshotModule.register_before_file_write_callback(
            lambda data: f"# a comment \n{data}"
        )

        module = SnapshotModule("tests.snapshots.snap_module", str(filepath))
        module["my_test"] = "result"

        SnapshotModule.clear_before_file_write_callbacks()
        module.save()

        with open(filepath) as snap_file:
            result = snap_file.read()

        assert "# a comment" not in result
        assert "my_test" in result
