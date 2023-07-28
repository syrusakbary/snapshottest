import unittest

import black
import snapshottest


def black_formatter_callback(data):
    return black.format_str(data, mode=black.Mode())


# Snapshot of this test will be formatted with black
snapshottest.module.SnapshotModule.register_before_file_write_callback(
    black_formatter_callback
)


class TestUsingCallback(snapshottest.TestCase):
    def setUp(self):
        pass

    def test_call_black(self):
        self.assertMatchSnapshot("some response to the test")


if __name__ == "__main__":
    unittest.main()
