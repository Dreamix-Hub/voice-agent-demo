from fastapi import Depends

from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.service import AppointmentService

from app.core.dependencies.customer import get_customer_service
from app.core.dependencies.business import get_business_service

from app.modules.customers.service import CustomerService
from app.modules.business.service import BusinessService


def get_appointment_repository() -> AppointmentRepository:
    return AppointmentRepository()


def get_appointment_service(
    customer_service: CustomerService = Depends(get_customer_service),
    business_service: BusinessService = Depends(get_business_service),
) -> AppointmentService:

    repository = get_appointment_repository()

    return AppointmentService(
        repository=repository,
        customer_service=customer_service,
        business_service=business_service,
    )