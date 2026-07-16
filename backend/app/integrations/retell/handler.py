from sqlalchemy.orm import Session
from uuid import UUID

from typing import cast

from app.integrations.retell.schemas import (
    RetellWebhook,
)
from app.modules.appointments.service import AppointmentService
from app.modules.conversations.dtos import (
    CompleteConversationCommand,
    StartConversationCommand,
    AttachConversationContentCommand
)
from app.modules.conversations.enums import ConversationProvider
from app.modules.conversations.service import ConversationService
from app.modules.customers.service import CustomerService


class RetellHandler:
    def __init__(
        self,
        conversation_service: ConversationService,
        customer_service: CustomerService,
    ):
        self.conversation_service = conversation_service
        self.customer_service = customer_service

    def handle_call_started(
        self,
        db: Session,
        webhook: RetellWebhook,
    ) -> None:
        """
        Handles the call_started event.

        - Finds or creates the customer using the caller's phone number.
        - Creates a new conversation.
        """

        if webhook.call.from_number is None:
            return

        if webhook.call.start_timestamp is None:
            return

        customer = self.customer_service.get_or_create_by_phone_number(
            db=db,
            phone_number=webhook.call.from_number,
        )

        customer_id = cast(UUID, customer.id)

        command = StartConversationCommand(
            customer_id=customer_id,
            provider=ConversationProvider.RETELL,
            external_call_id=webhook.call.call_id,
            started_at=webhook.call.start_timestamp,
        )

        self.conversation_service.start_conversation(
            db=db,
            command=command,
        )

    def handle_call_ended(
        self,
        db: Session,
        webhook: RetellWebhook,
    ) -> None:
        """
        Handles the call_ended event.

        Marks the conversation as completed.
        """

        if webhook.call.end_timestamp is None:
            return

        if webhook.call.duration_seconds is None:
            return

        command = CompleteConversationCommand(
            external_call_id=webhook.call.call_id,
            ended_at=webhook.call.end_timestamp,
            duration_seconds=webhook.call.duration_seconds,
        )

        self.conversation_service.complete_conversation(
            db=db,
            command=command,
        )

    def handle_call_analyzed(
        self,
        db: Session,
        webhook: RetellWebhook,
    ) -> None:
        """
        Handles the call_analyzed event.

        Stores transcript, AI summary and recording URL.
        """

        if webhook.call.transcript is None:
            return

        command = AttachConversationContentCommand(
            external_call_id=webhook.call.call_id,
            transcript=webhook.call.transcript,
            ai_summary=webhook.call.call_summary,
            recording_url=webhook.call.recording_url,
        )

        self.conversation_service.attach_content(
            db=db,
            command=command,
        )