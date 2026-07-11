from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CustomerCreate(BaseModel):
    name: str = Field(
    min_length=2,
    max_length=100,
    )
    phone: str = Field(
    min_length=8,
    max_length=20,
    )
    email: EmailStr | None = None
    notes: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    notes: str | None = None


class CustomerResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    email: EmailStr | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)