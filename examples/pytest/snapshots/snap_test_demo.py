# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot
from snapshottest.file import FileSnapshot


snapshots = Snapshot()

snapshots['test_me_endpoint 1'] = {
    'url': '/me'
}

snapshots['test_unicode 1'] = 'pépère'

snapshots['test_object 1'] = GenericRepr('SomeObject(3)')

snapshots['test_file 1'] = FileSnapshot('snap_test_demo/test_file 1.txt')

snapshots['test_multiple_files 1'] = FileSnapshot('snap_test_demo/test_multiple_files 1.txt')

snapshots['test_multiple_files 2'] = FileSnapshot('snap_test_demo/test_multiple_files 2.txt')

snapshots['test_nested_objects dict'] = {
    'key': GenericRepr('#')
}

snapshots['test_nested_objects defaultdict'] = {
    'key': [
        GenericRepr('#')
    ]
}

snapshots['test_nested_objects list'] = [
    GenericRepr('#')
]

snapshots['test_nested_objects tuple'] = (
    GenericRepr('#')
,)

snapshots['test_nested_objects set'] = set([
    GenericRepr('#')
])

snapshots['test_nested_objects frozenset'] = frozenset([
    GenericRepr('#')
])
