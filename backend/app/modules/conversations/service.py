from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.appointments.service import AppointmentService
from app.modules.conversations.enums import (
    ConversationProvider,
    ConversationStatus,
)
from app.common.exceptions import (
    ConversationNotFoundError,
    DuplicateConversationError,
)
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
        customer_id: uuid.UUID,
        provider: ConversationProvider,
        external_call_id: str,
        started_at: datetime,
    ) -> Conversation:
        """
        Called when the AI provider notifies us that a call has started.
        """

        customer = self.customer_service.get_customer(
            db=db,
            customer_id=customer_id,
        )

        if self.repository.exists_by_external_call_id(
            db=db,
            external_call_id=external_call_id,
        ):
            raise DuplicateConversationError()

        conversation = Conversation(
            customer_id=customer.id,
            provider=provider,
            external_call_id=external_call_id,
            status=ConversationStatus.STARTED,
            started_at=started_at,
        )

        return self.repository.create(
            db=db,
            conversation=conversation,
        )

    def complete_conversation(
        self,
        db: Session,
        *,
        external_call_id: str,
        ended_at: datetime,
        duration_seconds: int,
    ) -> Conversation:
        """
        Called when the call has finished.
        """

        conversation = self.get_by_external_call_id(
            db=db,
            external_call_id=external_call_id,
        )

        conversation.status = ConversationStatus.COMPLETED
        conversation.ended_at = ended_at
        conversation.duration_seconds = duration_seconds

        return self.repository.update(
            db=db,
            conversation=conversation,
        )

    def attach_content(
        self,
        db: Session,
        *,
        external_call_id: str,
        transcript: str,
        ai_summary: str | None,
        recording_url: str | None,
    ) -> Conversation:
        """
        Stores transcript, AI summary and recording URL after the call ends.
        """

        conversation = self.get_by_external_call_id(
            db=db,
            external_call_id=external_call_id,
        )

        if conversation.content is None:
            conversation.content = ConversationContent()

        conversation.content.transcript = transcript
        conversation.content.ai_summary = ai_summary
        conversation.content.recording_url = recording_url

        return self.repository.update(
            db=db,
            conversation=conversation,
        )

    def link_appointment(
        self,
        db: Session,
        *,
        external_call_id: str,
        appointment_id: uuid.UUID,
    ) -> Conversation:
        """
        Links an appointment created during the call to the conversation.
        """

        conversation = self.get_by_external_call_id(
            db=db,
            external_call_id=external_call_id,
        )

        appointment = self.appointment_service.get_appointment(
            db=db,
            appointment_id=appointment_id,
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
        Returns a conversation by external call ID or raises an exception.
        """

        conversation = self.repository.get_by_external_call_id(
            db=db,
            external_call_id=external_call_id,
        )

        if conversation is None:
            raise ConversationNotFoundError()

        return conversation