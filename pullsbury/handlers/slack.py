from slackclient import SlackClient
import logging
log = logging.getLogger(__name__)


class SlackHandler(object):
    def __init__(self, event, config):
        self.event = event
        self.slack = SlackClient(config.get('SLACK_AUTH_TOKEN'))
        self.channels_to_notify = self.parse_teams(config.get('TEAMS'), event.author)
        self.emojis = config.get('SLACK_EMOJIS')
        self.slack_icon = config.get('SLACK_ICON')

    def parse_teams(self, teams, author):
        channels = []

        for team_name, team in teams.iteritems():
            if author in team:
                channels.append({
                    'name': team_name,
                    'slack': team[author]['slack']
                })
                continue

        return channels

    def send_notifications(self):
        if not self.should_handle():
            return

        emoji = self.get_emoji(self.event.author)
        for channel in self.channels_to_notify:
            message = u"{} *A wild PR from @{} appeared!* {}\n_{}_: {}".format(
                emoji, channel['slack'], emoji, self.event.title, self.event.url
            )
            response = self.slack.api_call(
                "chat.postMessage",
                channel="#{}".format(channel['name']),
                text=message,
                username="Pullsbury Gitboy",
                icon_url=self.slack_icon,
                link_names=True,
                unfurl_links=True,
                mrkdwn=True
            )

            if not response['ok']:
                log.error(response)

    def should_handle(self):
        valid_actions = [
            "opened"
        ]

        if self.event.action not in valid_actions:
            return False

        if not self.event.pull_request:
            return False

        if not self.channels_to_notify:
            return False

        return True

    def get_emoji(self, author):
        name_index = len(author)
        for character in author:
            name_index = name_index + ord(character)
        emoji_index = name_index % len(self.emojis)

        return ":{}:".format(self.emojis[emoji_index])
