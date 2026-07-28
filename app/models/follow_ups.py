from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.sql import func

from app.core.database import Base


class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey(
            "customers.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    date = Column(
        Date,
        nullable=False,
        index=True
    )

    type = Column(
        String(50),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="pending",
        server_default="pending",
        index=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    reminder_sent_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )