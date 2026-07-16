from datetime import datetime

from .base import RetellWebhookBase


class CallEndedWebhook(RetellWebhookBase):
    call_id: str
    end_timestamp: datetime
    duration_seconds: int