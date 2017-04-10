# -*- coding: utf-8 -*-

# snapshottest: v1
# https://pypi.python.org/pypi/snapshottest

from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_me_endpoint 1'] = {
    'url': '/me'
}
