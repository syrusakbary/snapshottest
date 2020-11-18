import inspect
import sys
import unittest

from .diff import PrettyDiff
from .module import SnapshotModule, SnapshotTest
from .reporting import diff_report, reporting_lines


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
        test_name = self.test_id.split(".")[-1]
        return "{}::{} {}".format(class_name, test_name, self.curr_snapshot)


# Inspired by https://gist.github.com/twolfson/13f5f5784f67fd49b245
class TestCase(unittest.TestCase):

    # Whether snapshots should be updated, for all unittest-derived frameworks.
    # Set (perhaps circuitously) in runner init from the --snapshot-update
    # command line option. (.unittest.TestCase.snapshot_should_update is the
    # equivalent of pytest's config.option.snapshot_update.)
    snapshot_should_update = False

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
        if not (obj1 == obj2):
            raise self.failureException("\n".join(diff_report(obj1, obj2)))
        #     raise self.failureException("DIFF")

    @classmethod
    def tearDownClass(cls):
        if cls._snapshot_tests:
            module = SnapshotModule.get_module_for_testpath(cls._snapshot_file)
            module.save()
        super(TestCase, cls).tearDownClass()

    def setUp(self):
        """Do some custom setup"""
        # print dir(self.__module__)
        self.addTypeEqualityFunc(PrettyDiff, self.comparePrettyDifs)
        self._snapshot = UnitTestSnapshotTest(
            test_class=self.__class__,
            test_id=self.id(),
            test_filepath=self._snapshot_file,
            should_update=self.snapshot_should_update,
            assertEqual=self.assertEqual,
        )
        self._snapshot_tests.append(self._snapshot)
        SnapshotTest._current_tester = self._snapshot

    def tearDown(self):
        """Do some custom setup"""
        # print dir(self.__module__)
        SnapshotTest._current_tester = None
        self._snapshot = None

    def assert_match_snapshot(self, value, name=""):
        self._snapshot.assert_match(value, name=name)

    assertMatchSnapshot = assert_match_snapshot


def output_snapshottest_summary(stream=None, testing_cli=None):
    """
    Outputs a summary of snapshot tests for the session, if any.

    Call at the end of a test session to write results summary
    to stream (default sys.stderr). If no snapshot tests were run,
    outputs nothing.

    testing_cli (default from sys.argv) should be the string command
    line that invokes the tests, and is used to explain how to update
    snapshots.

    (This is the equivalent of .pytest.SnapshotSession.display,
    for unittest-derived frameworks.)
    """
    # TODO: Call this to replace near-duplicate code in .django and .nose.

    if not SnapshotModule.has_snapshots():
        return

    if stream is None:
        # This follows unittest.TextTestRunner, which by default uses sys.stderr
        # for test status and summary info (not sys.stdout).
        stream = sys.stderr
    if testing_cli is None:
        # We can't really recover the exact command line formatted for the user's shell
        # (quoting, etc.), but this should be close enough to get the point across.
        testing_cli = " ".join(sys.argv)

    separator1 = "=" * 70
    separator2 = "-" * 70

    print(separator1, file=stream)
    print("SnapshotTest summary", file=stream)
    print(separator2, file=stream)
    for line in reporting_lines(testing_cli):
        print(line, file=stream)
    print(separator1, file=stream)


def finalize_snapshots():
    """
    Call at the end of a unittest session to delete unused snapshots.

    (This deletes the data needed for SnapshotModule.total_unvisited_snapshots.
    Complete any reporting before calling this function.)
    """
    # TODO: this is duplicated in four places (with varying "should_update" conditions).
    #   Move it into shared code for snapshot sessions (which is currently implemented
    #   as classmethods on SnapshotModule).
    if TestCase.snapshot_should_update:
        for module in SnapshotModule.get_modules():
            module.delete_unvisited()
            module.save()


class SnapshotTestRunnerMixin:
    """
    A mixin for a unittest TestRunner that adds snapshottest session handling.

    Note: a TestRunner is not responsible for command line options. If you are
    adding snapshottest support to other unittest-derived frameworks, you must
    also arrange to set snapshottest.unittest.TestCase.snapshot_should_update
    when the user requests --snapshot-update.
    """

    def run(self, test):
        result = super().run(test)
        self.report_snapshottest_summary()
        finalize_snapshots()
        return result

    def report_snapshottest_summary(self):
        """Report a summary of snapshottest results for the session"""
        if hasattr(self, "stream"):
            # Mixed into a unittest.TextTestRunner or similar (with an output stream)
            output_snapshottest_summary(self.stream)
        else:
            # Mixed into some sort of graphical frontend, probably
            raise NotImplementedError(
                "Non-text TestRunner with SnapshotTestRunnerMixin"
                " must implement report_snapshottest_summary"
            )


class SnapshotTextTestRunner(SnapshotTestRunnerMixin, unittest.TextTestRunner):
    """
    Version of unittest.TextTestRunner that adds snapshottest session handling.
    """

    pass


class SnapshotTestProgram(unittest.TestProgram):
    """
    Augmented implementation of unittest.main that adds --snapshot-update
    command line option, and that ensures testRunner includes snapshottest
    session handling.
    """

    def __init__(self, *args, testRunner=None, **kwargs):
        # (For simplicity, we only allow testRunner as a kwarg.)
        if testRunner is None:
            testRunner = SnapshotTextTestRunner
        # Verify the testRunner includes snapshot session handling.
        # "The testRunner argument can either be a test runner class
        # or an already created instance of it."
        if not issubclass(testRunner, SnapshotTestRunnerMixin) and not isinstance(
            testRunner, SnapshotTestRunnerMixin
        ):
            raise TypeError(
                "snapshottest testRunner must include SnapshotTestRunnerMixin"
            )

        self._snapshot_update = False
        super().__init__(*args, testRunner=testRunner, **kwargs)

    def _getParentArgParser(self):
        # (Yes, this is hooking a private method. Sorry.
        # unittest.TestProgram isn't really designed to be extended.)
        parser = super()._getParentArgParser()
        parser.add_argument(
            "--snapshot-update",
            dest="_snapshot_update",
            action="store_true",
            help="Update snapshottest snapshots",
        )
        return parser

    def runTests(self):
        TestCase.snapshot_should_update = self._snapshot_update
        super().runTests()


main = SnapshotTestProgram
