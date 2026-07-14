from http import HTTPStatus

from app.common.exceptions.base import AppException


class AppointmentNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Appointment not found.",
            code="APPOINTMENT_NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )


class AppointmentConflictError(AppException):
    def __init__(self):
        super().__init__(
            message="The selected time slot is already booked.",
            code="APPOINTMENT_CONFLICT",
            status_code=HTTPStatus.CONFLICT,
        )


class OutsideBusinessHoursError(AppException):
    def __init__(self):
        super().__init__(
            message="The appointment time is outside business hours.",
            code="OUTSIDE_BUSINESS_HOURS",
            status_code=HTTPStatus.BAD_REQUEST,
        )


class BusinessInactiveError(AppException):
    def __init__(self):
        super().__init__(
            message="The business is currently inactive.",
            code="BUSINESS_INACTIVE",
            status_code=HTTPStatus.BAD_REQUEST,
        )


class AppointmentCompletedError(AppException):
    def __init__(self):
        super().__init__(
            message="Completed appointments cannot be modified.",
            code="APPOINTMENT_COMPLETED",
            status_code=HTTPStatus.BAD_REQUEST,
        )
