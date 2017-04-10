from __future__ import absolute_import
import pytest

from .module import SnapshotModule, SnapshotTest


def pytest_addoption(parser):
    group = parser.getgroup('snapshottest')
    group.addoption(
        '--snapshot-update',
        action='store_true',
        dest='snapshot_update',
        help='Update the snapshots.'
    )


class PyTestSnapshotTest(SnapshotTest):

    def __init__(self, request=None):
        self.request = request
        super(PyTestSnapshotTest, self).__init__()

    @property
    def module(self):
        return SnapshotModule.get_module_for_testpath(self.request.node.fspath.strpath)

    @property
    def update(self):
        return self.request.config.option.snapshot_update

    @property
    def test_name(self):
        return '{} {}'.format(
            self.request.node.name,
            self.curr_snapshot
        )


@pytest.fixture
def snapshot(request):
    with PyTestSnapshotTest(request) as snapshot_test:
        yield snapshot_test
