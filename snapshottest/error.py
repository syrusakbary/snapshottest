class SnapshotError(Exception):
    pass


class SnapshotNotFound(SnapshotError):
    def __init__(self, module, test_name):
        super(SnapshotNotFound, self).__init__(
            "Snapshot '{snapshot_id!s}' not found in {snapshot_file!s}".format(
                snapshot_id=test_name, snapshot_file=module.filepath
            )
        )
