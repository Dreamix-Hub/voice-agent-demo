from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BusinessCreate(BaseModel):
    business_name: str = Field(min_length=2, max_length=150)
    phone: str = Field(min_length=8, max_length=20)
    email: EmailStr | None = None
    address: str | None = None
    timezone: str = "Asia/Karachi"
    opening_time: time
    closing_time: time
    appointment_duration: int = Field(default=30, ge=5, le=180)
    system_prompt: str
    voice_name: str = "Friendly Receptionist"
    is_active: bool = True


class BusinessUpdate(BaseModel):
    business_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    timezone: str | None = None
    opening_time: time | None = None
    closing_time: time | None = None
    appointment_duration: int | None = Field(default=None, ge=5, le=180)
    system_prompt: str | None = None
    voice_name: str | None = None
    is_active: bool | None = None


class BusinessResponse(BaseModel):
    id: UUID
    business_name: str
    phone: str
    email: EmailStr | None
    address: str | None
    timezone: str
    opening_time: time
    closing_time: time
    appointment_duration: int
    system_prompt: str
    voice_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)