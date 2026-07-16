from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.orm import Session
from app.database.dependencies import  get_db
from app.integrations.retell.dependencies import (
    get_retell_webhook_service,
)
from app.integrations.retell.schemas import RetellWebhook
from app.integrations.retell.services.webhook_service import (
    RetellWebhookService,
)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post(
    "/retell",
    status_code=status.HTTP_204_NO_CONTENT,
)
def retell_webhook(
    webhook: RetellWebhook,
    db: Session = Depends(get_db),
    webhook_service: RetellWebhookService = Depends(
        get_retell_webhook_service,
    ),
) -> Response:
    """
    Handles incoming Retell webhooks.
    """

    webhook_service.handle_webhook(
        db=db,
        webhook=webhook,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )