from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class CustomerActivity(Base):
    __tablename__ = "customer_activities"

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

    type = Column(
        String(50),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )