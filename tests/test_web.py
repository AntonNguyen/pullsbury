from pullsbury import web
from mock import patch
from nose.tools import eq_
from unittest import TestCase
import json

test_data = {
    'action': 'derp',
    'pull_request': {
        'number': '3',
        'head': {
            'repo': {
                'git_url': 'testing',
            },
        },
        'base': {
            'ref': 'master',
            'repo': {
                'name': 'testing',
                'git_url': 'git://github.com/antonnguyen/testing',
                'owner': {
                    'login': 'antonnguyen',
                },
            },
        },
    },
}


class WebTest(TestCase):

    def setUp(self):
        self.app = web.app.test_client()

    def test_ping(self):
        res = self.app.get('/ping')
        eq_("pullsbury: %s pong\n" % (web.version,), res.data)
