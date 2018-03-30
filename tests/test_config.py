from unittest import TestCase
from pullsbury.config import load_config
from nose.tools import eq_, ok_


def test_load_config():
    res = load_config()
    assert res['GITHUB_USER'].endswith, 'Exists and is stringy'

def test_load_config_handles_slack_emojis():
    expected_emojis = [
        "exclamation",
        "heart",
        "icecream",
        "joy_cat",
        "octocat",
        "rainbow",
        "smile",
        "snowflake",
        "snowman",
        "sparkles",
        "squirrel",
        "tada",
    ]

    res = load_config()
    actual_emojis = res.get('SLACK_EMOJIS')

    ok_(len(actual_emojis) > 0)
    eq_(actual_emojis, expected_emojis)

def test_load_config_handles_teams():
    expected_teams = {
        "Channel": {
            "Github Username": {
                "slack": "Slack username"
            }
        }
    }

    res = load_config()
    actual_teams = res.get('TEAMS')
    eq_(actual_teams, expected_teams)