"""Main entry point (for unittest with snapshottest support)"""

# This is here to support invoking snapshottest-augmented unittest via
# `python -m snapshottest ...` (paralleling unittest's own `python -m unittest ...`).
# It's copied almost directly from unittest.__main__.

import sys

if sys.argv[0].endswith("__main__.py"):
    import os.path

    # We change sys.argv[0] to make help message more useful
    # use executable without path, unquoted
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m snapshottest"
    del os

from .unittest import main

main(module=None)
