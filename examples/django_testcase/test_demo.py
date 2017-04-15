import unittest
import snapshottest
import os


def api_client_get(url):
    return {
        'url': url,
    }


class TestDemo(snapshottest.DjangoTestCase):
    def setUp(self):
        pass

    def test_api_me(self):
        my_api_response = api_client_get('/me')
        self.assertMatchSnapshot(my_api_response)


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    from django.conf import settings

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory',
        }
    }

    settings.configure(SECRET_KEY='1', DATABASES=DATABASES)

    execute_from_command_line([os.path.abspath(__file__), 'test', 'test_demo'])
