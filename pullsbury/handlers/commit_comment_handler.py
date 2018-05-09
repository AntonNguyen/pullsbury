from pullsbury.models.comment import Comment
from slackclient import SlackClient

import logging
log = logging.getLogger(__name__)



class CommitCommentHandler(object):
    def __init__(self, event, _):
        comment = event.get('comment', {})

        self.type = 'commit_comment'
        self.author = event.get('sender', {}).get('login')
        self.comment = comment.get('body', '')
        self.path = comment.get('path')
        self.line = comment.get('line')


    def handle(self):
        Comment(
            pull_request_id=None,
            type=self.type,
            author=self.author,
            comment=self.comment,
            path=self.path,
            line=self.line
        ).save()
