from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CheckAvailabilityRequest(BaseModel):
    """
    Request sent by an AI provider to retrieve available appointment slots.
    """

    business_id: UUID
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


class BookAppointmentRequest(BaseModel):
    """
    Request sent by the AI to book an appointment.
    """

    business_id: UUID
    customer_id: UUID
    start_time: datetime


class BookAppointmentResponse(BaseModel):
    """
    Response returned after successfully booking an appointment.
    """

    appointment_id: UUID
    start_time: datetime
    end_time: datetime


class CancelAppointmentRequest(BaseModel):
    appointment_id: UUID


class CancelAppointmentResponse(BaseModel):
    success: bool = True


class RescheduleAppointmentRequest(BaseModel):
    appointment_id: UUID
    new_start_time: datetime


class RescheduleAppointmentResponse(BaseModel):
    appointment_id: UUID
    start_time: datetime
    end_time: datetime