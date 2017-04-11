SnapshotTest
============

Snapshot testing is a way to test your APIs without writing actual test
cases.

1. A snapshot is a single state of your API, saved in a file.
2. You have a set of snapshots for your API endpoints.
3. Once you add a new feature, you can generate *automatically* new
   snapshots for the updated API.

|travis| |pypi|

Installation
------------

::

    $ pip install snapshottest

Usage with unittest/nose
------------------------

.. code:: python

    from snapshottest import TestCase

    class APITestCase(TestCase):
        def test_api_me(self):
            """Testing the API for /me"""
            my_api_response = api.client.get('/me')
            self.assertMatchSnapshot(my_api_response)

Check the `Unittest
example <https://github.com/syrusakbary/snapshottest/tree/master/examples/unittest>`__.
If you want to update the snapshots automatically you can use the
``--snapshot-update`` when running with nose.

Usage with pytest
-----------------

.. code:: python

    def test_mything(snapshot):
        """Testing the API for /me"""
        my_api_response = api.client.get('/me')
        snapshot.assert_match(my_api_response)

If you want to update the snapshots automatically you can use the
``--snapshot-update`` config.

Check the `Pytest
example <https://github.com/syrusakbary/snapshottest/tree/master/examples/pytest>`__.

Contributing
============

After cloning this repo, ensure dependencies are installed by running:

.. code:: sh

    pip install -e ".[test]"

After developing, the full test suite can be evaluated by running:

.. code:: sh

    py.test tests --cov=snapshottest

Notes
=====

This package is heavily insipired in `jest snapshot
testing <https://facebook.github.io/jest/docs/snapshot-testing.html>`__.

Reasons for use this package
============================

    Most of this content is taken from the `Jest snapshot
    blogpost <https://facebook.github.io/jest/blog/2016/07/27/jest-14.html>`__.

We want to make it as frictionless as possible to write good tests that
are useful. We observed that when engineers are provided with
ready-to-use tools, they end up writing more tests, which in turn
results in stable and healthy code bases.

However engineers frequently spend more time writing a test than the
component itself. As a result many people stopped writing tests
altogether which eventually led to instabilities.

A typical snapshot test case for a mobile app renders a UI component,
takes a screenshot, then compares it to a reference image stored
alongside the test. The test will fail if the two images do not match:
either the change is unexpected, or the screenshot needs to be updated
to the new version of the UI component.

Snapshot Testing with SnapshotTest
----------------------------------

A similar approach can be taken when it comes to testing your APIs.
Instead of rendering the graphical UI, which would require building the
entire app, you can use a test renderer to quickly generate a
serializable value for your API response.

License
-------

`MIT
License <https://github.com/syrusakbary/snapshottest/blob/master/LICENSE>`__

|coveralls|

.. |travis| image:: https://img.shields.io/travis/syrusakbary/snapshottest.svg?style=flat
   :target: https://travis-ci.org/syrusakbary/snapshottest
.. |pypi| image:: https://img.shields.io/pypi/v/snapshottest.svg?style=flat
   :target: https://pypi.python.org/pypi/snapshottest
.. |coveralls| image:: https://coveralls.io/repos/syrusakbary/snapshottest/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/syrusakbary/snapshottest?branch=master
