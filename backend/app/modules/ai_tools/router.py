from fastapi import APIRouter, Depends

from app.database.dependencies import Session, get_db
from app.modules.ai_tools.dependencies import (
    get_ai_tool_service
)
from app.modules.ai_tools.schemas import (
    CheckAvailabilityRequest,
    CheckAvailabilityResponse,
)
from app.modules.ai_tools.service import AIToolService

router = APIRouter(
    prefix="/ai-tools",
    tags=["AI Tools"],
)


@router.post(
    "/check-availability",
    response_model=CheckAvailabilityResponse,
)
def check_availability(
    request: CheckAvailabilityRequest,
    db: Session = Depends(get_db),
    service: AIToolService = Depends(
        get_ai_tool_service,
    ),
) -> CheckAvailabilityResponse:
    """
    Returns available appointment slots for a given business and date.
    """

    return service.check_availability(
        db=db,
        request=request,
    )