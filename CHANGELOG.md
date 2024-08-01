# Changelog

## 1.0.0a1

### New features

- Allow snapshot files to be modified before being written #149
- Add typed enums support for TypeFormatter #163
- Add support for python 3.12 by using importlib instead of imp #168

### Bug fixes

- adding super().setUp() call to unittest.TestCase #169

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

### New features

- Add named snapshots #18
- Add support for file snapshots #54
- Hide empty output in the Django test runner #60

### Bug fixes

- Fix snapshot-update with nose #19
- Fix comparisons again objects stored as GenericRepr #20
- Fix setting snapshot_should_update on other TestCases #33
- Fix using non-ASCII characters #31
- Fix fail silently when snapshot files are invalid #45
- Remove unused snapshots in the Django runner #43
- Fix python3 multiline unicode snapshots #46
- Fix checks against falsy snapshots #50
- Various fixes in GenericFormatter and collection formatters #82
- Fix pytest parameterize for multiline strings #87

### Other changes

- Documentation improvements.
- Add wheel distribution #11
- Combine build scripts into a Makemile #83
- Update fastdiff version


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
