import sys
import logging
import pkg_resources

from flask import Flask, request, Response
from pullsbury.config import load_config
from pullsbury.database import db
from pullsbury.database import commit_request_transaction
from pullsbury.handlers.commit_comment_handler import CommitCommentHandler
from pullsbury.handlers.issue_comment_handler import IssueCommentHandler
from pullsbury.handlers.pull_request_handler import PullRequestHandler
from pullsbury.handlers.pull_request_review_comment_handler import PullRequestReviewCommentHandler

config = load_config()
app = Flask("pullsbury")
app.config.update(config)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

app.after_request(commit_request_transaction)
db.init_app(app)

log = logging.getLogger(__name__)
version = pkg_resources.get_distribution('pullsbury').version

EVENT_PROCESSORS = {
    'pull_request.opened': [PullRequestHandler],
    'pull_request.edited': [PullRequestHandler],
    'pull_request.closed': [PullRequestHandler],
    'pull_request.reopened': [PullRequestHandler],

    'commit_comment.created': [CommitCommentHandler],
    'commit_comment.edited': [CommitCommentHandler],
    'commit_comment.deleted': [CommitCommentHandler],

    'pull_request_review_comment.created': [PullRequestReviewCommentHandler],
    'pull_request_review_comment.edited': [PullRequestReviewCommentHandler],
    'pull_request_review_comment.deleted': [PullRequestReviewCommentHandler],

    'issue_comment.created': [IssueCommentHandler],
    'issue_comment.edited': [IssueCommentHandler],
    'issue_comment.deleted': [IssueCommentHandler],

}


@app.route("/")
def ping():
    return "pullsbury: %s pong\n" % (version,)


@app.route("/notify", methods=["POST"])
def notify():
    try:
        event = request.json
        event_type = request.headers.get('X-Github-Event')
        event_action = event.get('action')

        processor = u"{}.{}".format(event_type, event_action)
        log.info("{} event received".format(processor))
        if processor in EVENT_PROCESSORS:
            handlers = EVENT_PROCESSORS[processor]
            for handler in handlers:
                handler = handler(event, config)
                handler.handle()
                log.info("{} event handled by {}".format(processor))
    except Exception:
        log.exception("Unable to process webhook")
        return Response(status=500)

    return Response(status=200)
