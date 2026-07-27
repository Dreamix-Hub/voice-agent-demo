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
from app.modules.ai_tools.schemas import (
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentResponse,
    CancelAppointmentRequest,
    RescheduleAppointmentResponse, 
    RescheduleAppointmentRequest
)

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

@router.post(
    "/book-appointment",
    response_model=BookAppointmentResponse,
)
def book_appointment(
    request: BookAppointmentRequest,
    db: Session = Depends(get_db),
    service: AIToolService = Depends(
        get_ai_tool_service,
    ),
) -> BookAppointmentResponse:
    return service.book_appointment(
        db=db,
        request=request,
    )

@router.post(
    "/cancel-appointment",
    response_model=CancelAppointmentResponse,
)
def cancel_appointment(
    request: CancelAppointmentRequest,
    db: Session = Depends(get_db),
    service: AIToolService = Depends(get_ai_tool_service),
) -> CancelAppointmentResponse:
    return service.cancel_appointment(
        db=db,
        request=request,
    )

@router.post(
    "/reschedule-appointment",
    response_model=RescheduleAppointmentResponse,
)
def reschedule_appointment(
    request: RescheduleAppointmentRequest,
    db: Session = Depends(get_db),
    service: AIToolService = Depends(get_ai_tool_service),
) -> RescheduleAppointmentResponse:
    return service.reschedule_appointment(
        db=db,
        request=request,
    )