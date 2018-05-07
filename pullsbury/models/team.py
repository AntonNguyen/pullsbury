from pullsbury.database import db
from sqlalchemy import (
    BigInteger,
    Column,
    TIMESTAMP,
    String,
    text
)
from sqlalchemy.orm import relationship


class Team(db.Model):
    __tablename__ = 'team'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    slack_channel = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    users = relationship("User", secondary="team_member", backref="team")