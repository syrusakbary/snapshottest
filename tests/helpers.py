from snapshottest.module import SnapshotModule, SnapshotTest


class GenericSnapshotTest(SnapshotTest):
    """A concrete SnapshotTest implementation for no particular testing framework"""

    def __init__(self, snapshot_module, update=False, current_test_id=None):
        self._generic_options = {
            'snapshot_module': snapshot_module,
            'update': update,
            'record_mode': 'all' if update else 'new_interactions',
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

    @property
    def record_mode(self):
        return self._generic_options["record_mode"]

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

