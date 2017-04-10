from __future__ import absolute_import
import pytest
import traceback
from termcolor import colored

from .module import SnapshotModule, SnapshotTest


def pytest_addoption(parser):
    group = parser.getgroup('snapshottest')
    group.addoption(
        '--snapshot-update',
        action='store_true',
        default=False,
        dest='snapshot_update',
        help='Update the snapshots.'
    )
    group.addoption(
        '--snapshot-verbose',
        action='store_true',
        default=False,
        help='Dump diagnostic and progress information.'
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


class SnapshotSession(object):
    def __init__(self, config):
        self.verbose = config.getoption("snapshot_verbose")
        self.config = config

    def display(self, tr):
        tr.write_line('Snapshot Summary:')

        successful_snapshots = SnapshotModule.stats_successful_snapshots()
        bold = ['bold']
        if successful_snapshots:
            tr.write_line((
                colored('\t> {} snapshots passed', attrs=bold) + '.'
            ).format(successful_snapshots))
        new_snapshots = SnapshotModule.stats_new_snapshots()
        if new_snapshots[0]:
            tr.write_line((
                colored('\t> {} snapshots written', 'green', attrs=bold) + ' in {} test suites.'
            ).format(*new_snapshots))
        inspect_str = colored(
            'Inspect your code or run with `pytest --snapshot-update` to update them.',
            'grey',
            attrs=bold
        )
        failed_snapshots = SnapshotModule.stats_failed_snapshots()
        if failed_snapshots[0]:
            tr.write_line((
                colored('\t> {} snapshots failed', 'red', attrs=bold) + ' in {} test suites. '
                + inspect_str
            ).format(*failed_snapshots), red=True)
        unvisited_snapshots = SnapshotModule.stats_unvisited_snapshots()
        if unvisited_snapshots[0]:
            tr.write_line((
                colored('\t> {} snapshots deprecated', 'yellow', attrs=bold) + ' in {} test suites. '
                + inspect_str
            ).format(*unvisited_snapshots))


@pytest.fixture
def snapshot(request):
    with PyTestSnapshotTest(request) as snapshot_test:
        yield snapshot_test


def pytest_terminal_summary(terminalreporter):
    terminalreporter.config._snapshotsession.display(terminalreporter)


def pytest_fixture_post_finalizer(fixturedef):
    if fixturedef._fixturemanager.config.option.snapshot_update:
        for module in SnapshotModule.get_modules():
            module.delete_unvisited()
            module.save()


@pytest.mark.trylast  # force the other plugins to initialise, fixes issue with capture not being properly initialised
def pytest_configure(config):
    config._snapshotsession = SnapshotSession(config)
    # config.pluginmanager.register(bs, "snapshottest")
