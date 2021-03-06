from slackclient import SlackClient
import logging
log = logging.getLogger(__name__)


class SlackHandler(object):
    def __init__(self, event, config):
        self.event = event
        self.slack = SlackClient(config.get('SLACK_AUTH_TOKEN'))
        self.channels_to_notify = self.parse_teams(config.get('TEAMS'), event.author)
        self.happy_emojis = config.get('HAPPY_SLACK_EMOJIS')
        self.slack_icon = config.get('SLACK_ICON')
        self.repo_blacklist = config.get('REPO_BLACKLIST')
        self.slack_custom_emoji_mapping = config.get('SLACK_CUSTOM_EMOJI_MAPPING', {})

    def parse_teams(self, teams, author):
        channels = []

        for team_name, team in teams.items():
            if author in team:
                channels.append({
                    'name': team_name,
                    'slack': team[author]['slack']
                })
                continue

        return channels

    def send_notifications(self):
        if not self.should_handle():
            return 0

        sent = 0
        emoji = self.get_emoji(self.event.author)
        for channel in self.channels_to_notify:
            message = u"{} *A wild PR from @{} appeared!* {}\n_{}_: {}".format(
                emoji, channel['slack'], emoji, self.event.title, self.event.url
            )
            result = self.send_slack_message(
                channel['name'], message)
            if result:
                sent += 1
        return sent

    def send_slack_message(self, channel, message):
        response = self.slack.api_call(
            "chat.postMessage",
            channel="#{}".format(channel),
            text=message,
            username="Pullsbury Gitboy",
            icon_url=self.slack_icon,
            link_names=True,
            unfurl_links=True,
            mrkdwn=True
        )

        if not response['ok']:
            log.error(response)
            return False

        log.info("Slack message posted to #{}".format(channel))
        return True

    def should_handle(self):
        valid_actions = [
            "opened"
        ]

        if self.event.action not in valid_actions:
            return False

        if self.event.repository in self.repo_blacklist:
            return False

        if not self.event.pull_request:
            return False

        if not self.channels_to_notify:
            return False

        return True

    def get_emoji(self, author):
        if not len(self.happy_emojis):
            return ":heart:"
        if self.slack_custom_emoji_mapping.get(author):
            return ":{}:".format(self.slack_custom_emoji_mapping[author])

        name_index = len(author)
        for character in author:
            name_index = name_index + ord(character)
        emoji_index = name_index % len(self.happy_emojis)

        return ":{}:".format(self.happy_emojis[emoji_index])

