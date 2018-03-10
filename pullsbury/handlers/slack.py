import logging
log = logging.getLogger(__name__)


class SlackHandler(object):
    def __init__(self, event):
        self.event = event

    def send_notification(self):
        log.info("hello world!")
