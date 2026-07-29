from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=False,
        index=True
    )

    phone = Column(
        String(20),
        nullable=False
    )

    company = Column(
        String(150),
        nullable=True
    )

    source = Column(
        String(100),
        nullable=False
    )

    # Lead lifecycle status
    #
    # Allowed values:
    # New
    # Contacted
    # Interested
    # Qualified
    # Converted
    # Lost
    
    status = Column(
        String(50),
        nullable=False,
        default="New"
    )

    assigned_to = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )