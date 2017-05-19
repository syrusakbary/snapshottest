from django.test.runner import DiscoverRunner
from django.test import TestCase as dTestCase
from .unittest import TestCase as uTestCase


class TestRunner(DiscoverRunner):

    def __init__(self, snapshot_update=False, **kwargs):
        super().__init__(**kwargs)
        TestCase.snapshot_should_update = snapshot_update

    @classmethod
    def add_arguments(cls, parser):
        super(TestRunner, cls).add_arguments(parser)
        parser.add_argument(
            '--snapshot-update', default=False, action='store_true',
            dest='snapshot_update', help='Update the snapshots automatically.',
        )


class TestCase(uTestCase, dTestCase):
    pass
