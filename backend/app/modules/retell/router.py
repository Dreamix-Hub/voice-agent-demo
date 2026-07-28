from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.retell.dependencies import get_retell_service
from app.modules.retell.schemas import (
    CallStartedRequest,
    CallEndedRequest,
    CallAnalyzedRequest,
)
from app.modules.retell.service import RetellService

router = APIRouter(
    prefix="/retell",
    tags=["Retell"],
)


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db),
    service: RetellService = Depends(get_retell_service),
):
    payload = await request.json()

    event = payload.get("event")

    if event == "call_started":
        service.handle_call_started(
            db=db,
            request=CallStartedRequest.model_validate(
                payload["call"]
            ),
        )
        return {"success": True}

    if event == "call_ended":
        service.handle_call_ended(
            db=db,
            request=CallEndedRequest.model_validate(
                payload["call"]
            ),
        )
        return {"success": True}

    if event == "call_analyzed":
        service.handle_call_analyzed(
            db=db,
            request=CallAnalyzedRequest.model_validate(
                payload["call"]
            ),
        )
        return {"success": True}

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported event: {event}",
    )