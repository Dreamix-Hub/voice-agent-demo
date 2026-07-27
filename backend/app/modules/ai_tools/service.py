from sqlalchemy.orm import Session

from app.modules.ai_tools.schemas import (
    CheckAvailabilityRequest,
    CheckAvailabilityResponse,
    AvailableSlot,
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    RescheduleAppointmentRequest,
    RescheduleAppointmentResponse
)
from app.modules.appointments.commands import (
    GetAvailableSlotsCommand,
)
from app.modules.appointments.service import AppointmentService
from app.core.dependencies.business import (
    get_business_service
)
from app.modules.appointments.schemas import AppointmentCreate
from app.modules.customers.service import CustomerService
from app.core.dependencies.conversation import ConversationService
from datetime import  timedelta
from typing import cast
from uuid import UUID

class AIToolService:
    def __init__(
        self,
        appointment_service: AppointmentService,
        customer_service: CustomerService,
        conversation_service: ConversationService,
    ):
        self.appointment_service = appointment_service
        self.customer_service = customer_service
        self.conversation_service = conversation_service
        
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
    
    def cancel_appointment(
    self,
    db: Session,
    *,
    request: CancelAppointmentRequest,
) -> CancelAppointmentResponse:
        """
        Cancels the customer's appointment for the given date.
        """
    
        conversation = self.conversation_service.get_by_external_call_id(
            db=db,
            external_call_id=request.external_call_id,
        )
    
        appointment = self.appointment_service.get_customer_appointment_by_date(
            db=db,
            customer_id=conversation.customer_id,
            appointment_date=request.appointment_date,
        )
    
        appointment = self.appointment_service.cancel_appointment(
            db=db,
            appointment_id=appointment.id,
        )
    
        return CancelAppointmentResponse(
            appointment_id=appointment.id,
            status=appointment.status,
        )
    
    def reschedule_appointment(
    self,
    db: Session,
    *,
    request: RescheduleAppointmentRequest,
) -> RescheduleAppointmentResponse:
        """
        Reschedules a customer's appointment.
        """

        conversation = self.conversation_service.get_by_external_call_id(
            db=db,
            external_call_id=request.external_call_id,
        )

        appointment = self.appointment_service.get_customer_appointment_by_date(
            db=db,
            customer_id=conversation.customer_id,
            appointment_date=request.current_appointment_date,
        )

        appointment = self.appointment_service.reschedule_appointment(
            db=db,
            appointment_id=appointment.id,
            appointment_date=request.new_appointment_date,
            start_time=request.new_start_time,
        )

        return RescheduleAppointmentResponse(
            appointment_id=appointment.id,
            appointment_date=appointment.appointment_date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status,
        )