import os
from pullsbury.config import load_config
from nose.tools import eq_, ok_, raises, assert_raises


def test_load_config():
    res = load_config()
    assert res['GITHUB_USER'].endswith, 'Exists and is stringy'


@raises(IOError)
def test_load_config_returns_io_error_if_setting_file_is_not_found():
    load_config(settings_file='./unknown.py')


def test_load_config_prioritizes_the_pullsbury_settings_env_variable():
    old_settings = os.environ.get('PULLSBURY_SETTINGS')
    os.environ['PULLSBURY_SETTINGS'] = './unknown.py'

    with assert_raises(IOError):
        load_config()

    if old_settings:
        os.environ['PULLSBURY_SETTINGS'] = old_settings
    else:
        del os.environ['PULLSBURY_SETTINGS']


def test_load_config_handles_happy_slack_emojis():
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
    actual_emojis = res.get('HAPPY_SLACK_EMOJIS')

    ok_(len(actual_emojis) > 0)
    eq_(actual_emojis, expected_emojis)


def test_load_config_handles_teams():
    expected_teams = {
        "Channel": {
            "github-username": {
                "slack": "slack-username"
            }
        }
    }

    res = load_config()
    actual_teams = res.get('TEAMS')
    eq_(actual_teams, expected_teams)


def test_load_config_repo_blacklist():
    expected_repos = [
        "org_name/blacklisted"
    ]

    res = load_config()
    actual_repos = res.get('REPO_BLACKLIST')

    ok_(len(actual_repos) > 0)
    eq_(actual_repos, expected_repos)
