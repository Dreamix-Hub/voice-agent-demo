from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.responses import SuccessResponse
from app.database.dependencies import get_db
from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentStatusUpdate,
    AppointmentUpdate
)
from app.modules.appointments.service import AppointmentService
from app.modules.business.repository import BusinessRepository
from app.modules.business.service import BusinessService
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.service import CustomerService
from uuid import UUID
from datetime import date


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

appointment_repository = AppointmentRepository()

customer_repository = CustomerRepository()
customer_service = CustomerService(customer_repository)

business_repository = BusinessRepository()
business_service = BusinessService(business_repository)

appointment_service = AppointmentService(
    repository=appointment_repository,
    customer_service=customer_service,
    business_service=business_service,
)

@router.post(
    "",
    response_model=SuccessResponse[AppointmentResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
):
    appointment = appointment_service.create_appointment(
        db=db,
        data=data,
    )

    return SuccessResponse(
        data=AppointmentResponse.model_validate(appointment)
    )
    
@router.get(
    "",
    response_model=SuccessResponse[list[AppointmentResponse]],
)
def get_all_appointments(
    db: Session = Depends(get_db),
):
    appointments = appointment_service.get_all_appointments(db)

    return SuccessResponse(
        data=[
            AppointmentResponse.model_validate(a)
            for a in appointments
        ]
    )

@router.get(
    "/{appointment_id}",
    response_model=SuccessResponse[AppointmentResponse],
)
def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    appointment = appointment_service.get_appointment(
        db,
        appointment_id,
    )

    return SuccessResponse(
        data=AppointmentResponse.model_validate(
            appointment
        )
    )
    
@router.put(
    "/{appointment_id}",
    response_model=SuccessResponse[AppointmentResponse],
)
def update_appointment(
    appointment_id: UUID,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    appointment = appointment_service.update_appointment(
        db=db,
        appointment_id=appointment_id,
        data=data,
    )

    return SuccessResponse(
        data=AppointmentResponse.model_validate(appointment)
    )

@router.patch(
    "/{appointment_id}/status",
    response_model=SuccessResponse[AppointmentResponse],
)
def update_status(
    appointment_id: UUID,
    data: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
):
    appointment = appointment_service.update_status(
        db=db,
        appointment_id=appointment_id,
        status=data.status,
    )

    return SuccessResponse(
        data=AppointmentResponse.model_validate(appointment)
    )
    
@router.patch(
    "/{appointment_id}/cancel",
    response_model=SuccessResponse[AppointmentResponse],
)
def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
):
    appointment = appointment_service.cancel_appointment(
        db=db,
        appointment_id=appointment_id,
    )

    return SuccessResponse(
        data=AppointmentResponse.model_validate(appointment)
    )

@router.get(
    "/date/{appointment_date}",
    response_model=SuccessResponse[list[AppointmentResponse]],
)
def get_appointments_by_date(
    appointment_date: date,
    db: Session = Depends(get_db),
):
    appointments = appointment_service.get_appointments_by_date(
        db,
        appointment_date,
    )

    return SuccessResponse(
        data=[
            AppointmentResponse.model_validate(a)
            for a in appointments
        ]
    )
    
@router.get(
    "/customer/{customer_id}",
    response_model=SuccessResponse[list[AppointmentResponse]],
)
def get_customer_appointments(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    appointments = appointment_service.get_customer_appointments(
        db,
        customer_id,
    )

    return SuccessResponse(
        data=[
            AppointmentResponse.model_validate(a)
            for a in appointments
        ]
    )