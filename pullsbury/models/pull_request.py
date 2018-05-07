from pullsbury.database import db
from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    TIMESTAMP,
    String,
    text
)


class PullRequest(db.Model):
    __tablename__ = 'pull_request'

    id = Column(BigInteger, primary_key=True)
    author = Column(ForeignKey("user.github_username"), nullable=False)
    title = Column(String(100), nullable=False, server_default='')
    state = Column(String(50), nullable=False, server_default='open', index=True)
    closed_at = Column(TIMESTAMP, nullable=True)
    merged_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
