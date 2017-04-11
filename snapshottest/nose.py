from __future__ import absolute_import
import logging
import os

from nose.plugins import Plugin

from .module import SnapshotModule
from .reporting import reporting_lines
from .unittest import TestCase

log = logging.getLogger('nose.plugins.snapshottest')


class SnapshotTestPlugin(Plugin):
    name = 'snapshottest'
    enabled = True

    separator1 = "=" * 70
    separator2 = "-" * 70

    def options(self, parser, env=os.environ):
        super(SnapshotTestPlugin, self).options(parser, env=env)
        parser.add_option(
            '--snapshot-update',
            action='store_true',
            default=False,
            dest='snapshot_update',
            help='Update the snapshots.'
        )
        parser.add_option(
            '--snapshot-disable',
            action='store_true',
            dest='snapshot_disable',
            default=False,
            help="Disable special SnapshotTest"
        )

    def configure(self, options, conf):
        super(SnapshotTestPlugin, self).configure(options, conf)
        self.snapshot_update = options.snapshot_update
        self.enabled = not options.snapshot_disable

    def wantClass(self, cls):
        if issubclass(cls, TestCase):
            cls._snapshot_should_update = self.snapshot_update

    def afterContext(self):
        if self.snapshot_update:
            for module in SnapshotModule.get_modules():
                module.delete_unvisited()
                module.save()

    def report(self, stream):
        if not SnapshotModule.has_snapshots():
            return

        stream.writeln(self.separator1)
        stream.writeln('SnapshotTest summary')
        stream.writeln(self.separator2)
        for line in reporting_lines('nosetests'):
            stream.writeln(line)
        stream.writeln(self.separator1)
