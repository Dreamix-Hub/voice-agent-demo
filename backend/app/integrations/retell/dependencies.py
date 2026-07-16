from fastapi import Depends

from app.integrations.retell.handler import RetellHandler
from app.integrations.retell.services.webhook_service import (
    RetellWebhookService,
)
from app.core.dependencies.appointment import (
    get_appointment_service,
)
from app.modules.appointments.service import AppointmentService
from app.core.dependencies.conversation import (
    get_conversation_service,
)
from app.modules.conversations.service import ConversationService
from app.core.dependencies.customer import (
    get_customer_service,
)
from app.modules.customers.service import CustomerService


def get_retell_handler(
    conversation_service: ConversationService = Depends(
        get_conversation_service,
    ),
    customer_service: CustomerService = Depends(
        get_customer_service,
    ),
    appointment_service: AppointmentService = Depends(
        get_appointment_service,
    ),
) -> RetellHandler:
    return RetellHandler(
        conversation_service=conversation_service,
        customer_service=customer_service,
        appointment_service=appointment_service,
    )


def get_retell_webhook_service(
    handler: RetellHandler = Depends(
        get_retell_handler,
    ),
) -> RetellWebhookService:
    return RetellWebhookService(
        handler=handler,
    )