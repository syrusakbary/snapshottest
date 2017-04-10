# -*- coding: utf-8 -*-

# snapshottest: v1
# https://pypi.python.org/pypi/snapshottest

from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestDemo::test_api_me 1'] = {
    'url': '/me'
}
