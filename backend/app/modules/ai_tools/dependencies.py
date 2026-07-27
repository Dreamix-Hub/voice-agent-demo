from fastapi import Depends

from app.modules.ai_tools.service import AIToolService
from app.core.dependencies.appointment import (
    get_appointment_service,
)
from app.modules.appointments.service import AppointmentService
from app.modules.customers.service import CustomerService
from app.core.dependencies.customer import (
    get_customer_service
)

def get_ai_tool_service(
    appointment_service: AppointmentService = Depends(
        get_appointment_service,
    ),
    customer_service: CustomerService = Depends(
        get_customer_service,
    ),
) -> AIToolService:
    return AIToolService(
        appointment_service=appointment_service,
        customer_service=customer_service
    )