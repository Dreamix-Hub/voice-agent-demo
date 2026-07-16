from sqlalchemy import String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(100))

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    appointments = relationship(
    "Appointment",
    back_populates="customer",
    cascade="all, delete-orphan",
)
    conversations = relationship(
    "Conversation",
    back_populates="customer",
)