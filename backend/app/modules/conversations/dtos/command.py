from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.modules.conversations.enums import ConversationProvider


class StartConversationCommand(BaseModel):
    model_config = ConfigDict(frozen=True)

    customer_id: UUID
    provider: ConversationProvider
    external_call_id: str
    started_at: datetime


class CompleteConversationCommand(BaseModel):
    model_config = ConfigDict(frozen=True)

    external_call_id: str
    ended_at: datetime
    duration_seconds: int


class AttachConversationContentCommand(BaseModel):
    model_config = ConfigDict(frozen=True)

    external_call_id: str
    transcript: str
    ai_summary: str | None = None
    recording_url: str | None = None


class LinkAppointmentCommand(BaseModel):
    model_config = ConfigDict(frozen=True)

    external_call_id: str
    appointment_id: UUID