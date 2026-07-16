from enum import StrEnum


class RetellWebhookEvent(StrEnum):
    CALL_STARTED = "call_started"
    CALL_ENDED = "call_ended"
    CALL_ANALYZED = "call_analyzed"