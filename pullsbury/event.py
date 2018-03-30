import logging
log = logging.getLogger(__name__)


class Event(object):
    def __init__(self, request):
        try:
            self.type = request.headers.get('X-Github-Event')
            self.event = request.json
            self.action = self.event.get('action').lower()
            self.pull_request = self.event.get('pull_request', {})
            self.title = self.pull_request.get('title', '')
            self.url = self.pull_request.get('html_url', '')
            self.author = self.pull_request.get('user', {}).get('login', '')
        except Exception as e:
            log.error("Error processing event. '%s'", e)
            raise Exception()
