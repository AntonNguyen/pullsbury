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
        event = request.json
        action = event.get('action')
    except Exception as e:
        log.error("Got an invalid JSON body. '%s'", e)
        return Response(status=403,
                        response="You must provide a valid JSON body")
    try:
        processor = u"{}.{}".format(event_type, action)
        if processor in EVENT_PROCESSORS:
            handlers = EVENT_PROCESSORS[processor]
            for handler in handlers:
                handler = handler(event)
                handler.send_notification()
    except Exception:
        log.exception(u"Error processing event: {}".format(request.data))
        return Response(status=500)

    return Response(status=200)
