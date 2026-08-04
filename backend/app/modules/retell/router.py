import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.retell.dependencies import (
    get_retell_service,
    get_retell_webhook_verifier,
)
from app.modules.retell.schemas import (
    CallStartedRequest,
    CallEndedRequest,
    CallAnalyzedRequest,
)
from app.modules.retell.service import RetellService
from app.modules.retell.verifier import (
    RetellWebhookVerifier,
)

router = APIRouter(
    prefix="/retell",
    tags=["Retell"],
)


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db),
    service: RetellService = Depends(get_retell_service),
    verifier: RetellWebhookVerifier = Depends(
        get_retell_webhook_verifier,
    ),
):
    # Read the raw request body
    raw_body = await request.body()
    body = raw_body.decode("utf-8")

    # Get the Retell signature header
    signature = request.headers.get(
        "X-Retell-Signature",
    )

    if signature is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Retell signature.",
        )

    # Verify webhook authenticity
    try:
        verifier.verify(
            payload=body,
            signature=signature,
        )
    except Exception:
        raise HTTPException(
            status_code=401,
        )

    # Parse the verified payload
    payload = json.loads(body)

    event = payload.get("event")

    if event == "call_started":
        print(json.dumps(payload, indent=2))   # <------------- temporary logging purpose
        
        service.handle_call_started(
            db=db,
            request=CallStartedRequest.model_validate(
                payload["call"],
            ),
        )
        return {"success": True}

    if event == "call_ended":
        service.handle_call_ended(
            db=db,
            request=CallEndedRequest.model_validate(
                payload["call"],
            ),
        )
        return {"success": True}

    if event == "call_analyzed":
        service.handle_call_analyzed(
            db=db,
            request=CallAnalyzedRequest.model_validate(
                payload["call"],
            ),
        )
        return {"success": True}

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported event: {event}",
    )