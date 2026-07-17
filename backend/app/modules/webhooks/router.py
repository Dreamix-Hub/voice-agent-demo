from fastapi import APIRouter, Depends, Response, status, Request

from sqlalchemy.orm import Session
from app.database.dependencies import  get_db
from app.integrations.retell.dependencies import (
    get_retell_webhook_service,
)
from app.integrations.retell.services.webhook_service import (
    RetellWebhookService,
)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)

@router.post("/retell", status_code=status.HTTP_204_NO_CONTENT)
async def retell_webhook(
    request: Request,
    db: Session = Depends(get_db),
    webhook_service: RetellWebhookService = Depends(
        get_retell_webhook_service,
    ),
) -> Response:

    payload = await request.body()

    signature = request.headers.get(
        "X-Retell-Signature",
        "",
    )

    webhook_service.handle_webhook(
        db=db,
        payload=payload,
        signature=signature,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )