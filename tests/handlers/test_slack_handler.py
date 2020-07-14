from nose.tools import eq_, ok_
from pullsbury.handlers.slack_handler import SlackHandler
from pullsbury.models.event import Event
from pullsbury.config import load_config
from tests import load_fixture
from unittest import TestCase
from mock import Mock, patch
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

    def test_should_handle_returns_false_if_repo_is_blacklisted(self):
        event = TestableEvent(repository='org_name/blacklisted')
        self.config.update({
            'REPO_BLACKLIST': ['org_name/blacklisted']
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
            'HAPPY_SLACK_EMOJIS': []
        })
        handler = SlackHandler(event, self.config)
        eq_(handler.get_emoji('anton'), ':heart:')

    def test_get_emoji_returns_correct_custom_emoji(self):
        event = TestableEvent()
        self.config.update({
            'SLACK_CUSTOM_EMOJI_MAPPING': {
                'batman': 'joker'
            }
        })

        handler = SlackHandler(event, self.config)
        eq_(handler.get_emoji('batman'), ':joker:')
        # non custom emojis return the default response
        eq_(handler.get_emoji('anton'), ':sparkles:')
        eq_(handler.get_emoji('nguyen'), ':snowman:')

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
            {'name': 'rocket', 'slack': 'meowth'},
            {'name': 'team-catchem', 'slack': 'meowth'},
        ])

    def test_send_notifications_is_successful(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)

        mock_slack = self.mock_slack_response()
        handler.slack.api_call = mock_slack
        sent = handler.send_notifications()
        eq_(sent, 1)

        ok_(mock_slack.called)
        mock_slack.assert_called_with(
            'chat.postMessage',
            channel='#Channel',
            icon_url='https://i.imgur.com/oEL0h26.jpg',
            link_names=True,
            mrkdwn=True,
            text=u':snowflake: *A wild PR from @slack-username appeared!* :snowflake:\n_title_: http://api.github.com/repos/dev/emojis/pulls/2964',
            unfurl_links=True,
            username='Pullsbury Gitboy')

    @patch('pullsbury.handlers.slack_handler.SlackClient')
    def test_send_notifications_does_nothing_in_silent_mode(self, mock_slack_class):
        event = TestableEvent()
        self.config['SLACK_SILENT'] = True
        handler = SlackHandler(event, self.config)

        mock_slack = mock_slack_class.return_value
        handler.send_notifications()
        mock_slack.api_call.assert_not_called()

    def test_send_notifications_when_slack_call_fails(self):
        event = TestableEvent()
        handler = SlackHandler(event, self.config)

        mock_slack = self.mock_slack_response(
            fixture='responses/slack_post_message_failure.json')
        handler.slack.api_call = mock_slack

        sent = handler.send_notifications()
        eq_(sent, 0)
        ok_(mock_slack.called)

    def test_send_notifications_ignores_events_it_should_not_handle(self):
        event = TestableEvent(action='closed')
        handler = SlackHandler(event, self.config)
        sent = handler.send_notifications()
        eq_(sent, 0)

    def mock_slack_response(self, fixture='responses/slack_post_message_success.json'):
        mock_slack = Mock()
        mock_slack.return_value = json.loads(load_fixture(fixture))
        return mock_slack


class TestableEvent(Event):
    def __init__(self,
                 action='opened',
                 title='title',
                 url='http://api.github.com/repos/dev/emojis/pulls/2964',
                 author='github-username',
                 pull_request={'foo': 'bar'},
                 repository='dev/emojis'):

        self.action = action
        self.pull_request = pull_request
        self.title = title
        self.url = url
        self.author = author
        self.repository = repository
