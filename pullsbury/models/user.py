from pullsbury.database import db
from sqlalchemy import (
    BigInteger,
    Column,
    TIMESTAMP,
    String,
    text
)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    github_username = Column(String(50), nullable=False, index=True)
    slack_username = Column(String(50), nullable=False, index=True)
    first_name = Column(String(50), nullable=False, server_default='')
    last_name = Column(String(50), nullable=False, server_default='')
    email = Column(String(100), nullable=False, server_default='')
    custom_emoji = Column(String(50), nullable=False, server_default='')
    type = Column(String(10), nullable=False, server_default='human')
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
