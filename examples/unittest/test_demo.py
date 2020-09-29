import unittest
import snapshottest


def api_client_get(url):
    return {
        "url": url,
    }


class TestDemo(snapshottest.TestCase):
    def setUp(self):
        pass

    def test_api_me(self):
        my_api_response = api_client_get("/me")
        self.assertMatchSnapshot(my_api_response)


if __name__ == "__main__":
    unittest.main()
