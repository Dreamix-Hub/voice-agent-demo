from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.appointments.models import AppointmentStatus


class AppointmentCreate(BaseModel):
    customer_id: UUID
    appointment_date: date
    start_time: time
    reason: str = Field(min_length=3, max_length=255)
    notes: str | None = None


class AppointmentUpdate(BaseModel):
    appointment_date: date | None = None
    start_time: time | None = None
    reason: str | None = Field(default=None, min_length=3, max_length=255)
    notes: str | None = None


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentResponse(BaseModel):
    id: UUID
    customer_id: UUID
    appointment_date: date
    start_time: time
    end_time: time
    status: AppointmentStatus
    reason: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)