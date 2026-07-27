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
from app.modules.ai_tools.schemas import (
    BookAppointmentRequest,
    BookAppointmentResponse,
)
from app.modules.appointments.schemas import AppointmentCreate
from app.modules.customers.service import CustomerService
from datetime import  timedelta
from typing import cast
from uuid import UUID

class AIToolService:
    def __init__(
        self,
        appointment_service: AppointmentService,
        customer_service: CustomerService,
    ):
        self.appointment_service = appointment_service
        self.customer_service = customer_service
        
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
        
    def book_appointment(
        self,
        db: Session,
        *,
        request: BookAppointmentRequest,
) -> BookAppointmentResponse:
        """
            Books an appointment for the customer associated with
            the active conversation.
        """

        customer = self.customer_service.get_or_create_by_phone(
            db=db,
            phone_number=request.phone_number
        )

        appointment = self.appointment_service.create_appointment(
            db=db,
            data=AppointmentCreate(
                customer_id=cast(UUID, customer.id),
                appointment_date=request.appointment_date,
                start_time=request.start_time,
                reason=request.reason,
                notes=request.notes,
        ),
    )

        return BookAppointmentResponse(
            appointment_id=appointment.id,
            appointment_date=appointment.appointment_date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status,
    )