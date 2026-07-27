from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from app.modules.appointments.service import AppointmentStatus

class CheckAvailabilityRequest(BaseModel):
    """
    Request sent by an AI provider to retrieve available appointment slots.
    """

    target_date: date


class AvailableSlot(BaseModel):
    """
    Represents a single available appointment slot.
    """

    start_time: datetime
    end_time: datetime


class CheckAvailabilityResponse(BaseModel):
    """
    Response returned to the AI provider.
    """

    available_slots: list[AvailableSlot] = Field(default_factory=list)

class RescheduleAppointmentRequest(BaseModel):
    appointment_id: UUID
    new_start_time: datetime


class RescheduleAppointmentResponse(BaseModel):
    appointment_id: UUID
    start_time: datetime
    end_time: datetime
    
class BookAppointmentRequest(BaseModel):
    phone_number: str
    appointment_date: date
    start_time: time
    reason: str
    notes: str | None = None


class BookAppointmentResponse(BaseModel):
    appointment_id: UUID
    appointment_date: date
    start_time: time
    end_time: time
    status: AppointmentStatus

class CancelAppointmentRequest(BaseModel):
    external_call_id: str
    appointment_date: date


class CancelAppointmentResponse(BaseModel):
    appointment_id: UUID
    status: AppointmentStatus