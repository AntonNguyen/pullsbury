import logging
log = logging.getLogger(__name__)


class Event(object):
    def __init__(self, request):
        try:
            event_type = request.headers.get('X-Github-Event')
            self.type = event_type if event_type else ''
            self.event = request.json

            action = self.event.get('action')
            self.action = action.lower() if action else ''
            self.pull_request = self.event.get('pull_request', {})
            self.title = self.pull_request.get('title', '')
            self.url = self.pull_request.get('html_url', '')
            self.author = self.pull_request.get('user', {}).get('login', '')
            self.repository = self.event.get('repository', {}).get('full_name', '')
        except Exception as e:
            log.error("Error processing event. '%s'", e)
            raise Exception()
