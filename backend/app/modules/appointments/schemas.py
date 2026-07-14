from datetime import date, time

from pydantic import BaseModel, Field
from uuid import UUID


class AppointmentCreate(BaseModel):
    customer_id: UUID
    appointment_date: date
    start_time: time
    reason: str = Field(
        min_length=3,
        max_length=255,
    )
    notes: str | None = None