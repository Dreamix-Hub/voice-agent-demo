from http import HTTPStatus

from app.common.exceptions.base import AppException


class CustomerAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            message="Customer with this phone number already exists.",
            code="CUSTOMER_ALREADY_EXISTS",
            status_code=HTTPStatus.CONFLICT,
        )


class CustomerNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Customer not found.",
            code="CUSTOMER_NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )