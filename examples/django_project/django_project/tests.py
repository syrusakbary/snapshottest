import unittest

from snapshottest.django import SimpleTestCase


def api_client_get(url):
    return {
        "url": url,
    }


class TestDemo(SimpleTestCase):
    def test_api_me(self):
        my_api_response = api_client_get("/me")
        self.assertMatchSnapshot(my_api_response)


if __name__ == "__main__":
    unittest.main()
