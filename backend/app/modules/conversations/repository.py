from __future__ import annotations

import uuid

from sqlalchemy.orm import Session, joinedload

from app.modules.conversations.models import Conversation


class ConversationRepository:

    def create(
        self,
        db: Session,
        conversation: Conversation,
    ) -> Conversation:
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def update(
        self,
        db: Session,
        conversation: Conversation,
    ) -> Conversation:
        db.commit()
        db.refresh(conversation)
        return conversation

    def get_by_id(
        self,
        db: Session,
        conversation_id: uuid.UUID,
    ) -> Conversation | None:
        return (
            db.query(Conversation)
            .options(joinedload(Conversation.content))
            .filter(Conversation.id == conversation_id)
            .first()
        )

    def get_by_external_call_id(
        self,
        db: Session,
        external_call_id: str,
    ) -> Conversation | None:
        return (
            db.query(Conversation)
            .options(joinedload(Conversation.content))
            .filter(
                Conversation.external_call_id == external_call_id
            )
            .first()
        )

    def get_by_customer(
        self,
        db: Session,
        customer_id: uuid.UUID,
    ) -> list[Conversation]:
        return (
            db.query(Conversation)
            .filter(
                Conversation.customer_id == customer_id
            )
            .order_by(Conversation.started_at.desc())
            .all()
        )

    def get_recent(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Conversation]:
        return (
            db.query(Conversation)
            .order_by(Conversation.started_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete(
        self,
        db: Session,
        conversation: Conversation,
    ) -> None:
        db.delete(conversation)
        db.commit()
    
    def exists_by_external_call_id(
        self,
        db: Session,
        external_call_id: str,
    ) -> bool:
        return (
            db.query(Conversation.id)
            .filter(
                Conversation.external_call_id == external_call_id
        )
        .first()
        is not None
    )