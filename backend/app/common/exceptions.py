class AppException(Exception):
    """Base exception for all business exceptions."""

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)


class CustomerAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            message="Customer with this phone number already exists.",
            code="CUSTOMER_ALREADY_EXISTS",
        )


class CustomerNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Customer not found.",
            code="CUSTOMER_NOT_FOUND",
        )