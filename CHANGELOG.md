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