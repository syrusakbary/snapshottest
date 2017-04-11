from __future__ import absolute_import
import unittest
import inspect

from .module import SnapshotModule, SnapshotTest
from .diff import PrettyDiff
from .reporting import diff_report


class UnitTestSnapshotTest(SnapshotTest):

    def __init__(self, test_class, test_id, test_filepath, should_update, assertEqual):
        self.test_class = test_class
        self.test_id = test_id
        self.test_filepath = test_filepath
        self.assertEqual = assertEqual
        self.should_update = should_update
        super(UnitTestSnapshotTest, self).__init__()

    @property
    def module(self):
        return SnapshotModule.get_module_for_testpath(self.test_filepath)

    @property
    def update(self):
        return self.should_update

    def assert_equals(self, value, snapshot):
        self.assertEqual(value, snapshot)

    @property
    def test_name(self):
        class_name = self.test_class.__name__
        test_name = self.test_id.split('.')[-1]
        return '{}::{} {}'.format(
            class_name,
            test_name,
            self.curr_snapshot
        )


# Inspired by https://gist.github.com/twolfson/13f5f5784f67fd49b245
class TestCase(unittest.TestCase):

    _snapshot_should_update = False

    @classmethod
    def setUpClass(cls):
        """On inherited classes, run our `setUp` method"""
        cls._snapshot_tests = []
        cls._snapshot_file = inspect.getfile(cls)

        if cls is not TestCase and cls.setUp is not TestCase.setUp:
            orig_setUp = cls.setUp
            orig_tearDown = cls.tearDown

            def setUpOverride(self, *args, **kwargs):
                TestCase.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            def tearDownOverride(self, *args, **kwargs):
                TestCase.tearDown(self)
                return orig_tearDown(self, *args, **kwargs)

            cls.setUp = setUpOverride
            cls.tearDown = tearDownOverride

        super(TestCase, cls).setUpClass()

    def comparePrettyDifs(self, obj1, obj2, msg):
        # self
        # assert obj1 == obj2
        if not(obj1 == obj2):
            raise self.failureException('\n'.join(diff_report(obj1, obj2)))
        #     raise self.failureException("DIFF")

    @classmethod
    def tearDownClass(cls):
        if cls._snapshot_tests:
            module = SnapshotModule.get_module_for_testpath(cls._snapshot_file)
            module.save()

    def setUp(self):
        """Do some custom setup"""
        # print dir(self.__module__)
        self.addTypeEqualityFunc(PrettyDiff, self.comparePrettyDifs)
        self._snapshot = UnitTestSnapshotTest(
            test_class=self.__class__,
            test_id=self.id(),
            test_filepath=self._snapshot_file,
            should_update=self._snapshot_should_update,
            assertEqual=self.assertEqual
        )
        self._snapshot_tests.append(self._snapshot)
        SnapshotTest._current_tester = self._snapshot

    def tearDown(self):
        """Do some custom setup"""
        # print dir(self.__module__)
        SnapshotTest._current_tester = None
        self._snapshot = None

    def assert_match_snapshot(self, value):
        self._snapshot.assert_match(value)

    assertMatchSnapshot = assert_match_snapshot
