from slackclient import SlackClient
import logging
log = logging.getLogger(__name__)


class PullRequestHandler(object):
    def __init__(self, event, _):
        self.event = event

    def handle(self):
        return