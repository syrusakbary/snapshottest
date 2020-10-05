import snapshottest


def api_client_get(url):
    return {
        "url": url,
    }


# Use snapshottest.TestCase in place of unittest.TestCase
# where you want to run snapshot tests.
#
# (You can also mix it into any subclass of unittest.TestCase:
#   class TestDemo(snapshottest.TestCase, MyCustomTestCase):
# ...)
class TestDemo(snapshottest.TestCase):
    def setUp(self):
        pass

    def test_api_me(self):
        my_api_response = api_client_get("/me")
        self.assertMatchSnapshot(my_api_response)


if __name__ == "__main__":
    # Replace unittest.main() with snapshottest's version:
    # unittest.main()
    snapshottest.main()
