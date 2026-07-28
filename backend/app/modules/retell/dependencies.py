from fastapi import Depends

from app.core.dependencies.conversation import (
    get_conversation_service,
)
from app.modules.conversations.service import ConversationService
from app.core.dependencies.customer import (
    get_customer_service,
)
from app.modules.customers.service import CustomerService
from app.modules.retell.service import RetellService

from app.core.config import settings
from app.modules.retell.verifier import (
    RetellWebhookVerifier,
)


def get_retell_service(
    customer_service: CustomerService = Depends(
        get_customer_service,
    ),
    conversation_service: ConversationService = Depends(
        get_conversation_service,
    ),
) -> RetellService:
    return RetellService(
        customer_service=customer_service,
        conversation_service=conversation_service,
    )



def get_retell_webhook_verifier() -> RetellWebhookVerifier:
    return RetellWebhookVerifier(
        api_key=settings.RETELL_API_KEY,
    )