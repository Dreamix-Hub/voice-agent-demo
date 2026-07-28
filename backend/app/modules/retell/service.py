from sqlalchemy.orm import Session

from app.modules.conversations.dtos import (
    StartConversationCommand,
    CompleteConversationCommand,
    AttachConversationContentCommand,
)
from app.modules.conversations.enums import ConversationProvider
from app.modules.conversations.service import ConversationService
from app.modules.customers.service import CustomerService
from app.modules.retell.schemas import (
    CallStartedRequest,
    CallEndedRequest,
    CallAnalyzedRequest,
)
from typing import cast
from uuid import UUID


class RetellService:
    def __init__(
        self,
        customer_service: CustomerService,
        conversation_service: ConversationService,
    ):
        self.customer_service = customer_service
        self.conversation_service = conversation_service

    def handle_call_started(
        self,
        db: Session,
        *,
        request: CallStartedRequest,
    ) -> None:
        """
        Creates (or retrieves) the customer and starts
        a new conversation.
        """

        customer = self.customer_service.get_or_create_by_phone(
            db=db,
            phone_number=request.from_number,
        )

        self.conversation_service.start_conversation(
            db=db,
            command=StartConversationCommand(
                customer_id=cast(UUID, customer.id),
                provider=ConversationProvider.RETELL,
                external_call_id=request.call_id,
                started_at=request.started_at,
            ),
        )

    def handle_call_ended(
        self,
        db: Session,
        *,
        request: CallEndedRequest,
    ) -> None:
        """
        Marks the conversation as completed and stores
        the transcript and recording.
        """

        self.conversation_service.complete_conversation(
            db=db,
            command=CompleteConversationCommand(
                external_call_id=request.call_id,
                ended_at=request.ended_at,
                duration_seconds=request.duration_seconds,
            ),
        )

        self.conversation_service.attach_content(
            db=db,
            command=AttachConversationContentCommand(
                external_call_id=request.call_id,
                transcript=request.transcript,
                ai_summary=None,
                recording_url=request.recording_url,
            ),
        )

    def handle_call_analyzed(
        self,
        db: Session,
        *,
        request: CallAnalyzedRequest,
    ) -> None:
        """
        Stores the AI-generated call summary.
        """

        self.conversation_service.attach_content(
            db=db,
            command=AttachConversationContentCommand(
                external_call_id=request.call_id,
                transcript="",
                ai_summary=request.ai_summary,
                recording_url=None,
            ),
        )