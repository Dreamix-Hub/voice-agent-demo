from sqlalchemy.orm import Session

from app.integrations.retell.handler import RetellHandler
from app.integrations.retell.schemas import (
    RetellWebhook,
    RetellWebhookEvent,
)


class RetellWebhookService:
    def __init__(
        self,
        handler: RetellHandler,
    ):
        self.handler = handler

    def handle_webhook(
        self,
        db: Session,
        *,
        webhook: RetellWebhook,
    ) -> None:
        """
        Dispatches incoming Retell webhook events to the appropriate handler.
        """

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
                # Ignore unsupported events
                return