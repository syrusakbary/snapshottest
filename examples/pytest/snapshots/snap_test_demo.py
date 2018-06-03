# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_me_endpoint 1'] = {
    'url': '/me'
}

snapshots['test_unicode 1'] = u'p\xe9p\xe8re'
