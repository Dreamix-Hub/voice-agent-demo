from datetime import datetime

from .base import RetellWebhookBase


class CallStartedWebhook(RetellWebhookBase):
    call_id: str
    from_number: str
    to_number: str
    start_timestamp: datetime