from pullsbury.models.pull_request import PullRequest
from pullsbury.models.comment import Comment
from slackclient import SlackClient

import logging
log = logging.getLogger(__name__)



class IssueCommentHandler(object):
    def __init__(self, event, _):
        self.type = 'issue_comment'
        self.author = event.get('sender', {}).get('login')

    def handle(self):
        Comment(
            pull_request_id=None,
            type=self.type,
            author=self.author,
            comment=self.comment,
            path=self.path,
            line=self.line
        ).save()
