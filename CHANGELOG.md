# Changelog

## 1.0.0a0

### BREAKING CHANGES

- Require Python 3.5+


## 0.6.0

### New features

- Sort written snapshots.
- Extract Django TestRunner to a mixin so it can be used with alternative base
  classes.

### Bug fixes

- Handle SortedDict with keys other than strings.
- Fix error when snapshotting mock Calls objects.
- Fix formatting of `float("nan")` and `float("inf")`.
- Adopt a valid PEP-508 version range for fastdiff.

### Other changes

- Documentation improvements.
- Add tests and changelog to sdist.


## 0.5.1

Changelog not available. (Pull request welcome!)


## 0.5.0

* Add django support. Closes #1
    - Add `snapshottest.django.TestRunner`
    - Add `snapshottest.django.TestCase`
    - Add `--snapshot-update` to django test command. You can use `python manage.py test --snapshot-update`
* Fix #3, all dicts are sorted before saving it and before comparing.

### Breaking changes

* Drop support for `python 3.3`. Since django don't support that version of python.
* Since all dicts are sorted, this cloud be a breaking change for your tests.
    Use the `--snapshot-update` option to update your tests
