from pullsbury.database import db
from sqlalchemy import (
    Column,
    ForeignKey,
    TIMESTAMP,
    String,
    text
)


class TeamMember(db.Model):
    __tablename__ = 'team_member'

    team_id = Column(ForeignKey("team.id"), primary_key=True, nullable=False)
    user_id = Column(ForeignKey("user.id"), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
