# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestDemo::test_api_me 1'] = {
    'url': '/me'
}
