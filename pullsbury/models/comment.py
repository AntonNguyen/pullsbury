from pullsbury.database import db
from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    TIMESTAMP,
    String,
    text
)
from sqlalchemy.orm import relationship


class Comment(db.Model):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True)
    author = Column(ForeignKey("user.github_username"), nullable=False)
    comment = Column(String(255), nullable=False, server_default='')
    pull_request_id = Column(BigInteger, ForeignKey('pull_request.id'))
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    pull_request = relationship("PullRequest", backref="comment")
