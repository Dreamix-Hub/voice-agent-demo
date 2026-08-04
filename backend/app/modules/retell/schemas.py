from datetime import datetime
from pydantic import BaseModel


class CallStartedRequest(BaseModel):
    call_id: str
    from_number: str
    call_type: str
    started_at: datetime


class CallEndedRequest(BaseModel):
    call_id: str
    ended_at: datetime
    duration_seconds: int
    transcript: str
    recording_url: str | None = None


class CallAnalyzedRequest(BaseModel):
    call_id: str
    ai_summary: str | None = None