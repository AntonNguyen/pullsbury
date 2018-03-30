from . import load_fixture
from mock import patch
from nose.tools import eq_, ok_
from pullsbury import web
from unittest import TestCase


class WebTest(TestCase):

    def setUp(self):
        self.app = web.app.test_client()

    def test_ping(self):
        res = self.app.get('/')
        eq_("pullsbury: %s pong\n" % (web.version,), res.data)

    def test_notify_invalid_request(self):
        res = self.app.post('/notify',
                            content_type='application/json',
                            data='')
        eq_(res.status_code, 500)
        eq_('', res.data)

    def test_notify_handles_valid_request(self):
        res = self.app.post('/notify',
                            content_type='application/json',
                            data=load_fixture('pull_request_opened.json'))
        eq_(res.status_code, 200)
        eq_('', res.data)

    @patch('pullsbury.web.SlackHandler.send_notifications')
    def test_notify_makes_request_to_slack(self, mock_send_notifications):
        res = self.app.post('/notify',
                            content_type='application/json',
                            headers={
                                'X-Github-Event': 'pull_request'
                            },
                            data=load_fixture('pull_request_opened.json'))

        eq_(res.status_code, 200)
        eq_('', res.data)
        ok_(mock_send_notifications.called)

    @patch('pullsbury.web.SlackHandler.send_notifications')
    def test_notify_ignores_edited_events(self, mock_send_notifications):
        res = self.app.post('/notify',
                            content_type='application/json',
                            headers={
                                'X-Github-Event': 'pull_request'
                            },
                            data=load_fixture('pull_request_edited.json'))

        eq_(res.status_code, 200)
        eq_('', res.data)
        ok_(mock_send_notifications.notCalled)