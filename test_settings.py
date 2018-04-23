import os
import json


def env(key, default, cast=str):
    return cast(os.environ.get(key, default))


# Webserver configuration #
###########################

# gunicorn config
bind = env('PULLSBURY_GUNICORN_BIND', '127.0.0.1:5000')
debug = env('PULLSBURY_GUNICORN_DEBUG', True, bool)
loglevel = env('PULLSBURY_GUNICORN_LOGLEVEL', 'debug')

# Config file for logging
LOGGING_CONFIG = './logging.ini'

# General project configuration #
#################################

# Use GITHUB_URL when working with github:e
# When working with github:e don't forget to add the /api/v3 path
GITHUB_URL = env('GITHUB_URL', 'http://api.github.com')

# Github username + password
# This is the user that pullsbury will use
# to fetch repositories and leave review comments.
# Set the GITHUB_PASSWORD environment variable first.
# example: $ export GITHUB_PASSWORD=mygithubpassword
GITHUB_USER = env('GITHUB_USERNAME', 'octocat')
GITHUB_PASSWORD = env('GITHUB_PASSWORD', '')

# You can also use an Oauth token for github, if you do
# uncomment this line. Using a token will take precedence
# over a username and password.
GITHUB_OAUTH_TOKEN = env('GITHUB_OAUTH_TOKEN', None)

# Slack settings
SLACK_AUTH_TOKEN = env('SLACK_AUTH_TOKEN', '')
SLACK_ICON = env('SLACK_ICON', 'https://i.imgur.com/oEL0h26.jpg')
HAPPY_SLACK_EMOJIS = env('HAPPY_SLACK_EMOJIS', json.dumps([
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
]))

SLACK_CUSTOM_EMOJI_MAPPING = env('SLACK_CUSTOM_EMOJI_MAPPING', json.dumps({
    "author": "custom_emoji"
}))

# Teams. Expected Format:
#
# {
#     "Team Slack Channel": {
#         "Github username": {
#             "slack": "Slack username"
#         }
#     }
# }
TEAMS = env('TEAMS', json.dumps({
    "Channel": {
        "github-username": {
            "slack": "slack-username"
        }
    }
}))

# List of repos to not notify
REPO_BLACKLIST = env('REPO_BLACKLIST', json.dumps([
    'org_name/blacklisted'
]))
