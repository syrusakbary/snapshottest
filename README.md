# PySnap [![travis][travis-image]][travis-url] [![pypi][pypi-image]][pypi-url]

[travis-image]: https://travis-ci.com/yourbuddyconner/pysnap.svg?style=flat
[travis-url]: https://travis-ci.org/yourbuddyconner/pysnap
[pypi-image]: https://img.shields.io/pypi/v/pysnap.svg?style=flat
[pypi-url]: https://pypi.python.org/pypi/pysnap


**Note:** This project is just a fork of the package `snapshottest` which lives [here](https://github.com/syrusakbary/snapshottest). It had been mostly abandoned, so I kicked the wheels and got it back in working order. Contributions are welcome! 

Snapshot testing is a way to test your APIs without writing actual test cases.

1. A snapshot is a single state of your API, saved in a file.
2. You have a set of snapshots for your API endpoints.
3. Once you add a new feature, you can *automatically* generate new snapshots for the updated API.


## Installation

    $ pip install pysnap


## Usage with unittest/nose

```python
from pysnap import TestCase

class APITestCase(TestCase):
    def test_api_me(self):
        """Testing the API for /me"""
        my_api_response = api.client.get('/me')
        self.assertMatchSnapshot(my_api_response)

        # Set custom snapshot name: `gpg_response`
        my_gpg_response = api.client.get('/me?gpg_key')
        self.assertMatchSnapshot(my_gpg_response, 'gpg_response')
```

If you want to update the snapshots automatically you can use the `nosetests --snapshot-update`.

Check the [Unittest example](https://github.com/yourbuddyconner/pysnap/tree/master/examples/unittest).

## Usage with pytest

```python
def test_mything(snapshot):
    """Testing the API for /me"""
    my_api_response = api.client.get('/me')
    snapshot.assert_match(my_api_response)

    # Set custom snapshot name: `gpg_response`
    my_gpg_response = api.client.get('/me?gpg_key')
    snapshot.assert_match(my_gpg_response, 'gpg_response')
```

If you want to update the snapshots automatically you can use the `--snapshot-update` config.

Check the [Pytest example](https://github.com/yourbuddyconner/pysnap/tree/master/examples/pytest).

## Usage with django
Add to your settings:
```python
TEST_RUNNER = 'pysnap.django.TestRunner'
```
To create your snapshot test:
```python
from pysnap.django import TestCase

class APITestCase(TestCase):
    def test_api_me(self):
        """Testing the API for /me"""
        my_api_response = api.client.get('/me')
        self.assertMatchSnapshot(my_api_response)
```
If you want to update the snapshots automatically you can use the `python manage.py test --snapshot-update`.
Check the [Django example](https://github.com/yourbuddyconner/pysnap/tree/master/examples/django_project).

# Contributing

After cloning this repo, ensure dependencies are installed by running:

```sh
pip install -e ".[test]"
```

After developing, the full test suite can be evaluated by running:

```sh
py.test
```


# Notes

This package is heavily insipired in [jest snapshot testing](https://facebook.github.io/jest/docs/snapshot-testing.html).

# Reasons for use this package

> Most of this content is taken from the [Jest snapshot blogpost](https://facebook.github.io/jest/blog/2016/07/27/jest-14.html).

We want to make it as frictionless as possible to write good tests that are useful.
We observed that when engineers are provided with ready-to-use tools, they end up writing more tests, which in turn results in stable and healthy code bases.

However engineers frequently spend more time writing a test than the component itself. As a result many people stopped writing tests altogether which eventually led to instabilities.

A typical snapshot test case for a mobile app renders a UI component, takes a screenshot, then compares it to a reference image stored alongside the test. The test will fail if the two images do not match: either the change is unexpected, or the screenshot needs to be updated to the new version of the UI component.


## Snapshot Testing with PySnap

A similar approach can be taken when it comes to testing your APIs.
Instead of rendering the graphical UI, which would require building the entire app, you can use a test renderer to quickly generate a serializable value for your API response.


## License

[MIT License](https://github.com/yourbuddyconner/pysnap/blob/master/LICENSE)
