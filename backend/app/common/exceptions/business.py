from http import HTTPStatus

from app.common.exceptions.base import AppException


class BusinessAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            message="Business profile already exists.",
            code="BUSINESS_ALREADY_EXISTS",
            status_code=HTTPStatus.CONFLICT,
        )


class BusinessNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Business profile not found.",
            code="BUSINESS_NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )