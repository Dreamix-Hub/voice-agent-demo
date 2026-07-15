from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import (
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)
from app.modules.conversations.enums import (
    ConversationProvider,
    ConversationStatus,
)


class Conversation(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "conversations"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False,
    )

    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id"),
        unique=True,
        nullable=True,
    )

    provider: Mapped[ConversationProvider] = mapped_column(
        Enum(ConversationProvider),
        nullable=False,
    )

    external_call_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus),
        nullable=False,
        default=ConversationStatus.STARTED,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Relationships
    customer = relationship(
        "Customer",
        back_populates="conversations",
    )

    appointment = relationship(
        "Appointment",
        back_populates="conversation",
    )

    content = relationship(
        "ConversationContent",
        back_populates="conversation",
        uselist=False,
        cascade="all, delete-orphan",
    )