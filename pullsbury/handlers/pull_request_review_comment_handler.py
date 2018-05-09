from pullsbury.database import db
from pullsbury.models.pull_request import PullRequest
from pullsbury.models.comment import Comment
from slackclient import SlackClient

import logging
log = logging.getLogger(__name__)



class PullRequestReviewCommentHandler(object):
    def __init__(self, event, _):
        comment = event.get('comment', {})
        pull_request = event.get('pull_request', {})
        self.pull_request_id = pull_request.get('id')
        self.pull_request_title = pull_request.get('title')
        self.pull_request_author = pull_request.get('user', {}).get('login', '')


        self.type = 'pull_request_review_comment'
        self.author = event.get('sender', {}).get('login')

        self.comment = comment.get('body', '')
        self.path = comment.get('path')
        self.line = comment.get('line')


    def handle(self):
        pull_request = db.query(PullRequest).filter_by(id=self.pull_request_id))
        if not pull_request:
            PullRequest(
                id=self.pull_request_id,
                title=self.pull_request_title,
                author=self.pull_request_author
            ).save()
        Comment(
            pull_request_id=self.pull_request_id,
            type=self.type,
            author=self.author,
            comment=self.comment,
            path=self.path,
            line=self.line
        ).save()