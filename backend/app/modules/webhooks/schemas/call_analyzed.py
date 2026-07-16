from .base import RetellWebhookBase


class CallAnalyzedWebhook(RetellWebhookBase):
    call_id: str
    transcript: str
    summary: str | None = None
    recording_url: str | None = None