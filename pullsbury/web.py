import json
import logging
import pkg_resources

from flask import Flask, request, Response
from pullsbury.config import load_config
from pullsbury.github import get_client
from pullsbury.handlers.slack import SlackHandler

config = load_config()
app = Flask("pullsbury")
app.config.update(config)

log = logging.getLogger(__name__)
version = pkg_resources.get_distribution('pullsbury').version

EVENT_PROCESSORS = {
    'pull_request.opened': [SlackHandler]
}


@app.route("/")
def ping():
    return "pullsbury: %s pong\n" % (version,)


@app.route("/notify", methods=["POST"])
def notify():
    try:
        event_type = request.headers.get('X-Github-Event')
        event = json.load(request.data)
        action = event.get('action')

        processor = u"{}.{}".format(event_type, action)
        if processor in EVENT_PROCESSORS:
            handler = EVENT_PROCESSORS[processor](event)
            handler.send_notification()
    except Exception:
        log.exception(u"Error handling event: {}".format(request.data))

    return Response(200)
