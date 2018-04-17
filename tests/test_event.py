from . import load_fixture
from nose.tools import eq_
from pullsbury.models.event import Event
from unittest import TestCase
import json

class TestEvent(TestCase):
    def test_event_parse(self):
        request = MockRequest(
            headers={
                'X-Github-Event': 'opened'
            },
            body=load_fixture('requests/pull_request_opened.json'))
        event = Event(request)
        eq_(event.type, 'opened')
        eq_(event.action, 'opened')
        eq_(event.title, 'Add more emojis')
        eq_(event.url, 'https://github.example.com/org_name/emojis/pull/2964')
        eq_(event.author, 'github-username')

    def test_non_pull_request_event_parse(self):
        request = MockRequest(
            body=load_fixture('requests/non_pull_request_event.json'))
        event = Event(request)
        eq_(event.type, '')
        eq_(event.action, '')
        eq_(event.title, '')
        eq_(event.url, '')
        eq_(event.author, '')


class MockRequest(object):
    def __init__(self, headers={}, body=''):
        self.headers = headers
        self.json = json.loads(body)