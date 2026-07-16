from http import HTTPStatus

from app.common.exceptions.base import AppException


class ConversationNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Conversation not found.",
            code="CONVERSATION_NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )


class DuplicateConversationError(AppException):
    def __init__(self):
        super().__init__(
            message="A conversation with this external call ID already exists.",
            code="DUPLICATE_CONVERSATION",
            status_code=HTTPStatus.CONFLICT,
        )


class ConversationAlreadyCompletedError(AppException):
    def __init__(self):
        super().__init__(
            message="Conversation has already been completed.",
            code="CONVERSATION_ALREADY_COMPLETED",
            status_code=HTTPStatus.CONFLICT,
        )


class ConversationContentAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            message="Conversation content already exists.",
            code="CONVERSATION_CONTENT_ALREADY_EXISTS",
            status_code=HTTPStatus.CONFLICT,
        )


class AppointmentAlreadyLinkedError(AppException):
    def __init__(self):
        super().__init__(
            message="An appointment is already linked to this conversation.",
            code="APPOINTMENT_ALREADY_LINKED",
            status_code=HTTPStatus.CONFLICT,
        )


class InvalidConversationStatusError(AppException):
    def __init__(self, status: str):
        super().__init__(
            message=f"Operation is not allowed when conversation status is '{status}'.",
            code="INVALID_CONVERSATION_STATUS",
            status_code=HTTPStatus.BAD_REQUEST,
        )