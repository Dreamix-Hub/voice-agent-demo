from fastapi import Depends

from app.core.dependencies.customer import get_customer_service
from app.core.dependencies.appointment import get_appointment_service

from app.modules.conversations.repository import ConversationRepository
from app.modules.conversations.service import ConversationService


def get_conversation_repository():
    return ConversationRepository()


def get_conversation_service(
    customer_service=Depends(get_customer_service),
    appointment_service=Depends(get_appointment_service),
):
    return ConversationService(
        repository=get_conversation_repository(),
        customer_service=customer_service,
        appointment_service=appointment_service,
    )