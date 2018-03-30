from . import load_fixture
from nose.tools import eq_
from pullsbury.event import Event
from unittest import TestCase
import json

class TestEvent(TestCase):
    def test_event_parse(self):
        request = MockRequest(
            headers={
                'X-Github-Event': 'opened'
            },
            body=load_fixture('pull_request_opened.json'))
        event = Event(request)
        eq_(event.type, 'opened')
        eq_(event.action, 'opened')
        eq_(event.title, 'Add more emojis')
        eq_(event.url, 'https://github.example.com/dev/emojis/pull/2964')
        eq_(event.author, 'github-username')


class MockRequest(object):
    def __init__(self, headers={}, body=''):
        self.headers = headers
        self.json = json.loads(body)