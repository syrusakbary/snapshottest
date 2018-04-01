# -*- coding: utf-8 -*-

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
