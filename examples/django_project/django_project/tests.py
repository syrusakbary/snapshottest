import unittest
from datetime import datetime

from snapshottest.django import TestCase


def api_client_get(url):
    return {
        'url': url,
    }


class TestDemo(TestCase):

    def test_api_me(self):
        # Note this tests should fail unless the snapshot-update command line
        # option is specified. Run  `python manage.py test --snapshot-update`.
        now = datetime.now().isoformat()
        my_api_response = api_client_get('/' + now)
        self.assertMatchSnapshot(my_api_response)


if __name__ == '__main__':
    unittest.main()
