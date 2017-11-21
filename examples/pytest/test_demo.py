# -*- coding: utf-8 -*-

import datetime


def api_client_get(url):
    return {
        'url': url,
    }


def test_me_endpoint(snapshot):
    """Testing the API for /me"""
    my_api_response = api_client_get('/me')
    snapshot.assert_match(my_api_response)


def test_unicode(snapshot):
    """Simple test with unicode"""
    expect = u'pépère'
    snapshot.assert_match(expect)


def test_datetime(snapshot):
    """Simple test with datetime"""
    expect = datetime.datetime(2017, 11, 19)
    snapshot.assert_match(expect)
