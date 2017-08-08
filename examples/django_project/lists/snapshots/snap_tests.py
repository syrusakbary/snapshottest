# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['ListTest::test_uses_home_template 1'] = '''<html>
    <title>Lists</title>
    <body>
      <table id="id_list_table">
        
        <tr><td>1: test</td></tr>
        
      </table>:

    </body>
</html>
'''
