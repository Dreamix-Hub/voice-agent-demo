from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RetellCall(BaseModel):
    """
    Represents the Retell Call object.

    Only the fields currently required by our application
    are modeled here.
    """

    model_config = ConfigDict(
        extra="allow",
    )

    call_id: str

    from_number: str | None = None

    to_number: str | None = None

    start_timestamp: datetime | None = None

    end_timestamp: datetime | None = None

    duration_seconds: int | None = None

    transcript: str | None = None

    recording_url: str | None = None

    call_summary: str | None = None