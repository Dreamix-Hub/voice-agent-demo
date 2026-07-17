from http import HTTPStatus

from app.common.exceptions.base import AppException


class InvalidWebhookSignatureError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid webhook signature.",
            code="INVALID_WEBHOOK_SIGNATURE",
            status_code=HTTPStatus.UNAUTHORIZED,
        )