import logging
import pkg_resources

from flask import Flask, request, Response
from pullsbury.config import load_config
from pullsbury.github import get_client
from pullsbury.tasks import notify_pull_request

config = load_config()
app = Flask("pullsbury")
app.config.update(config)

log = logging.getLogger(__name__)
version = pkg_resources.get_distribution('pullsbury').version


@app.route("/ping")
def ping():
    return "pullsbury: %s pong\n" % (version,)


@app.route("/review/start", methods=["POST"])
def start_review():
    event = request.headers.get('X-Github-Event')
    if event == 'ping':
        return Response(status=200)
