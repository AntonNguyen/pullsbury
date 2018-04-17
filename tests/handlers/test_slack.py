from tests import load_fixture
from mock import patch
from nose.tools import eq_, ok_
from pullsbury.handlers.slack_handler import SlackHandler
from pullsbury.models.event import Event
from pullsbury.config import load_config
from unittest import TestCase
import json

class TestSlackHandler(TestCase):
    def setUp(self):
        self.config = load_config()

    def test_should_handle_returns_false_if_invalid_action(self):
        event = TestableEvent(action='edited')
        handler = SlackHandler(event, self.config)
        ok_(not handler.should_handle())

    def test_should_handle_returns_false_if_there_is_no_pull_request_body(self):
        event = TestableEvent(pull_request=None)
        handler = SlackHandler(event, self.config)
        ok_(not handler.should_handle())

    def test_should_handle_returns_false_if_there_is_no_channel_to_notify(self):
        event = TestableEvent()
        self.config.update({
            'TEAMS': {}
        })
        handler = SlackHandler(event, self.config)
        ok_(not handler.should_handle())

    def test_should_handle_returns_true(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        ok_(handler.should_handle())

    def test_get_emoji_returns_same_emoji_for_author(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        eq_(handler.get_emoji('anton'), ':sparkles:')
        eq_(handler.get_emoji('nguyen'), ':snowman:')

    def test_get_emoji_returns_emoji_even_if_emoji_list_is_empty(self):
        event = TestableEvent()
        self.config.update({
            'SLACK_EMOJIS': []
        })
        handler = SlackHandler(event, self.config)
        eq_(handler.get_emoji('anton'), ':heart:')

    def test_parse_teams_returns_empty_list_if_no_teams_provided(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        teams = {}
        channels_to_notify = handler.parse_teams(teams, 'anton')
        eq_(channels_to_notify, [])

    def test_parse_teams_returns_an_empty_list_if_author_not_found(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        teams = {
            'rocket': {
                'jesse': {
                    'slack': 'jesse'
                },
                'james': {
                    'slack': 'james'
                },
                'meowth': {
                    'slack': 'mewoth'
                }
            }
        }
        channels_to_notify = handler.parse_teams(teams, 'ash')
        eq_(channels_to_notify, [])

    def test_parse_teams_returns_a_non_empty_list_if_author_found(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        teams = {
            'rocket': {
                'jesse': {
                    'slack': 'jesse'
                },
                'james': {
                    'slack': 'james'
                },
                'meowth': {
                    'slack': 'mewoth'
                }
            }
        }
        channels_to_notify = handler.parse_teams(teams, 'jesse')
        eq_(channels_to_notify, [{'name': 'rocket', 'slack': 'jesse'}])

    def test_parse_teams_returns_a_list_of_two_if_author_found_in_multiple_teams(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        teams = {
            'rocket': {
                'jesse': {
                    'slack': 'jesse'
                },
                'james': {
                    'slack': 'james'
                },
                'meowth': {
                    'slack': 'meowth'
                }
            },
            'team-catchem': {
                'ash': {
                    'slack': 'ash'
                },
                'meowth': {
                    'slack': 'meowth'
                }
            }
        }
        channels_to_notify = handler.parse_teams(teams, 'meowth')
        eq_(channels_to_notify, [
            {'name': 'team-catchem', 'slack': 'meowth'},
            {'name': 'rocket', 'slack': 'meowth'},
        ])

    @patch('pullsbury.handlers.slack_handler.SlackHandler.send_slack_message')
    def test_send_notifications(self, send_slack_message):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)
        handler.send_notifications()

        expected_message = u":snowflake: *A wild PR from @slack-username appeared!* :snowflake:\n_title_: http://api.github.com/repos/dev/emojis/pulls/2964"
        ok_(send_slack_message.called)
        send_slack_message.assert_called_with('Channel', expected_message)


class TestableEvent(Event):
    def __init__(self,
                 action='opened',
                 title='title',
                 url='http://api.github.com/repos/dev/emojis/pulls/2964',
                 author='github-username',
                 pull_request={'foo': 'bar'}):

        self.action = action
        self.pull_request = pull_request
        self.title = title
        self.url = url
        self.author = author