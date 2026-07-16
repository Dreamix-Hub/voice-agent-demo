from __future__ import annotations

from sqlalchemy.orm import Session

from app.common.exceptions import (
    ConversationAlreadyExistsError,
    ConversationNotFoundError,
)
from app.modules.appointments.service import AppointmentService
from app.modules.conversations.dtos import (
    AttachConversationContentCommand,
    CompleteConversationCommand,
    LinkAppointmentCommand,
    StartConversationCommand,
)
from app.modules.conversations.enums import ConversationStatus
from app.modules.conversations.models import (
    Conversation,
    ConversationContent,
)
from app.modules.conversations.repository import ConversationRepository
from app.modules.customers.service import CustomerService


class ConversationService:
    def __init__(
        self,
        repository: ConversationRepository,
        customer_service: CustomerService,
        appointment_service: AppointmentService,
    ):
        self.repository = repository
        self.customer_service = customer_service
        self.appointment_service = appointment_service

    def start_conversation(
        self,
        db: Session,
        *,
        command: StartConversationCommand,
    ) -> Conversation:
        """
        Creates a new conversation when an AI provider starts a call.
        """

        customer = self.customer_service.get_customer(
            db=db,
            customer_id=command.customer_id,
        )

        if self.repository.exists_by_external_call_id(
            db=db,
            external_call_id=command.external_call_id,
        ):
            raise ConversationAlreadyExistsError()

        conversation = Conversation(
            customer_id=customer.id,
            provider=command.provider,
            external_call_id=command.external_call_id,
            status=ConversationStatus.STARTED,
            started_at=command.started_at,
        )

        return self.repository.create(
            db=db,
            conversation=conversation,
        )

    def complete_conversation(
        self,
        db: Session,
        *,
        command: CompleteConversationCommand,
    ) -> Conversation:
        """
        Marks a conversation as completed.
        """

        conversation = self.get_by_external_call_id(
            db=db,
            external_call_id=command.external_call_id,
        )

        conversation.status = ConversationStatus.COMPLETED
        conversation.ended_at = command.ended_at
        conversation.duration_seconds = command.duration_seconds

        return self.repository.update(
            db=db,
            conversation=conversation,
        )

    def attach_content(
        self,
        db: Session,
        *,
        command: AttachConversationContentCommand,
    ) -> Conversation:
        """
        Stores transcript, AI summary and recording URL.
        """

        conversation = self.get_by_external_call_id(
            db=db,
            external_call_id=command.external_call_id,
        )

        if conversation.content is None:
            conversation.content = ConversationContent()

        conversation.content.transcript = command.transcript
        conversation.content.ai_summary = command.ai_summary
        conversation.content.recording_url = command.recording_url

        return self.repository.update(
            db=db,
            conversation=conversation,
        )

    def link_appointment(
        self,
        db: Session,
        *,
        command: LinkAppointmentCommand,
    ) -> Conversation:
        """
        Links an appointment to a conversation.
        """

        conversation = self.get_by_external_call_id(
            db=db,
            external_call_id=command.external_call_id,
        )

        appointment = self.appointment_service.get_appointment(
            db=db,
            appointment_id=command.appointment_id,
        )

        conversation.appointment_id = appointment.id

        return self.repository.update(
            db=db,
            conversation=conversation,
        )

    def get_by_external_call_id(
        self,
        db: Session,
        *,
        external_call_id: str,
    ) -> Conversation:
        """
        Returns a conversation by its external call ID.
        """

        conversation = self.repository.get_by_external_call_id(
            db=db,
            external_call_id=external_call_id,
        )

        if conversation is None:
            raise ConversationNotFoundError()

        return conversation