from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.core.dependencies.appointment import get_appointment_service
from app.core.dependencies.customer import get_customer_service

from app.modules.appointments.service import AppointmentService
from app.modules.conversations.repository import ConversationRepository
from app.modules.conversations.service import ConversationService
from app.modules.customers.service import CustomerService


def get_conversation_repository() -> ConversationRepository:
    return ConversationRepository()


def get_conversation_service(
    db: Session = Depends(get_db),
    customer_service: CustomerService = Depends(get_customer_service),
    appointment_service: AppointmentService = Depends(get_appointment_service),
) -> ConversationService:
    return ConversationService(
        repository=get_conversation_repository(),
        customer_service=customer_service,
        appointment_service=appointment_service,
    )