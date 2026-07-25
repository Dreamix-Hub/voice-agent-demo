from sqlalchemy.orm import Session

from app.modules.ai_tools.schemas import (
    CheckAvailabilityRequest,
    CheckAvailabilityResponse,
    AvailableSlot,
)
from app.modules.appointments.commands import (
    GetAvailableSlotsCommand,
)
from app.modules.appointments.service import AppointmentService
from app.core.dependencies.business import (
    get_business_service
)
from datetime import datetime, timedelta

class AIToolService:
    """
    Exposes business capabilities to AI providers
    such as Retell, OpenAI, or Vapi.
    """

    def __init__(
        self,
        appointment_service: AppointmentService,
    ):
        self.appointment_service = appointment_service

    def check_availability(
        self,
        db: Session,
        *,
        request: CheckAvailabilityRequest,
    ) -> CheckAvailabilityResponse:
        
        command = GetAvailableSlotsCommand(
            target_date=request.target_date,
        )

        slots = self.appointment_service.get_available_slots(
            db=db,
            command=command,
        )

        return CheckAvailabilityResponse(
            available_slots=[
                AvailableSlot(
                    start_time=slot,
                    end_time=slot + timedelta(minutes=get_business_service().get_business(db).appointment_duration),
                )
                for slot in slots
            ]
        )
