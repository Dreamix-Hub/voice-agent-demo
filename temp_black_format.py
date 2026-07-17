import json
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from app.integrations.retell.handler import RetellHandler
from app.integrations.retell.schemas import (
    RetellWebhook,
    RetellWebhookEvent,
)
from app.integrations.retell.verifier import RetellWebhookVerifier
class RetellWebhookService:
    def __init__(
        self,
        handler: RetellHandler,
        verifier: RetellWebhookVerifier,
    ):
        self.handler = handler
        self.verifier = verifier
        
    def handle_webhook(
    self,
    db: Session,
    *,
    payload: bytes,
    signature: str,
) -> None:
        self.verifier.verify(
            payload=payload,
            signature_header=signature,
        )

        webhook = TypeAdapter(
            RetellWebhook,
        ).validate_python(
            json.loads(payload),
        )

        match webhook.event:

            case RetellWebhookEvent.CALL_STARTED:
                self.handler.handle_call_started(
                    db=db,
                    webhook=webhook,
                )

            case RetellWebhookEvent.CALL_ENDED:
                self.handler.handle_call_ended(
                    db=db,
                    webhook=webhook,
                )

            case RetellWebhookEvent.CALL_ANALYZED:
                self.handler.handle_call_analyzed(
                    db=db,
                    webhook=webhook,
                )

            case _:
                return