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
    pull_request_id = Column(BigInteger, ForeignKey('pull_request.id'), nullable=True)
    type = Column(String(50), nullable=False)
    author = Column(ForeignKey("user.github_username"), nullable=False)
    comment = Column(String(255), nullable=False, server_default='')
    path = Column(String(255), nullable=True)
    line = Column(BigInteger, nullable=True)
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    pull_request = relationship("PullRequest", backref="comment")
