import pytest

from snapshottest.pytest import PyTestSnapshotTest


@pytest.fixture
def options():
    return {}


@pytest.fixture
def _apply_options(request, monkeypatch, options):
    for k, v in options.items():
        monkeypatch.setattr(request.config, k, v, raising=False)


@pytest.fixture
def pytest_snapshot_test(request, _apply_options):
    return PyTestSnapshotTest(request)


class TestPyTestSnapShotTest:
    def test_property_test_name(self, pytest_snapshot_test):
        pytest_snapshot_test.assert_match('counter')
        assert pytest_snapshot_test.test_name == \
            'TestPyTestSnapShotTest.test_property_test_name 1'

        pytest_snapshot_test.assert_match('named', 'named_test')
        assert pytest_snapshot_test.test_name == \
            'TestPyTestSnapShotTest.test_property_test_name named_test'

        pytest_snapshot_test.assert_match('counter')
        assert pytest_snapshot_test.test_name == \
            'TestPyTestSnapShotTest.test_property_test_name 2'


def test_pytest_snapshottest_property_test_name(pytest_snapshot_test):
    pytest_snapshot_test.assert_match('counter')
    assert pytest_snapshot_test.test_name == \
        'test_pytest_snapshottest_property_test_name 1'

    pytest_snapshot_test.assert_match('named', 'named_test')
    assert pytest_snapshot_test.test_name == \
        'test_pytest_snapshottest_property_test_name named_test'

    pytest_snapshot_test.assert_match('counter')
    assert pytest_snapshot_test.test_name == \
        'test_pytest_snapshottest_property_test_name 2'
