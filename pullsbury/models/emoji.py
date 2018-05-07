from pullsbury.database import db
from sqlalchemy import (
    Column,
    TIMESTAMP,
    String,
    text
)


class Emoji(db.Model):
    __tablename__ = 'emoji'

    name = Column(String(50), nullable=False, primary_key=True)
    sentiment = Column(String(10), nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
