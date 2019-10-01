import os
import sys
import json
import logging
import pkg_resources

from flask import Flask, request, Response
from pullsbury.config import load_config
from pullsbury.handlers.slack_handler import SlackHandler
from pullsbury.models.event import Event

config = load_config()
app = Flask("pullsbury")
app.config.update(config)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

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
        event = Event(request)
        processor = "{}.{}".format(event.type, event.action)
        log.info("{} event received from {}".format(processor, event.author))
        if processor in EVENT_PROCESSORS:
            handlers = EVENT_PROCESSORS[processor]
            for handler in handlers:
                handler = handler(event, config)
                handler.send_notifications()
                log.info("{} event handled by {}".format(processor, event.author))
    except Exception:
        log.exception("Unable to process webhook")
        return Response(status=500)

    return Response(status=200)
