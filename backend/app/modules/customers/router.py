from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.modules.customers.service import CustomerService
from app.common.responses import SuccessResponse

from pydantic import BaseModel

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

repository = CustomerRepository()
service = CustomerService(repository)

@router.post(
    "",
    response_model=SuccessResponse[CustomerResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    customer = service.create_customer(
        db,
        data,
    )

    return SuccessResponse(
        data=CustomerResponse.model_validate(customer),
    )

@router.get(
    "",
    response_model=SuccessResponse[list[CustomerResponse]],
)
def list_customers(
    db: Session = Depends(get_db),
):
    customers = service.list_customers(db)

    return SuccessResponse(
        data=[
            CustomerResponse.model_validate(customer)
            for customer in customers
        ]
    )

@router.get(
    "/{customer_id}",
    response_model=SuccessResponse[CustomerResponse],
)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    customer = service.get_customer(
        db,
        customer_id,
    )

    return SuccessResponse(
        data=CustomerResponse.model_validate(customer)
    )

@router.put(
    "/{customer_id}",
    response_model=SuccessResponse[CustomerResponse],
)
def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = service.update_customer(
        db,
        customer_id,
        data,
    )

    return SuccessResponse(
        data=CustomerResponse.model_validate(customer)
    )

class MessageResponse(BaseModel):
    message: str

@router.delete(
    "/{customer_id}",
    response_model=SuccessResponse[MessageResponse],
)
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    service.delete_customer(
        db,
        customer_id,
    )

    return SuccessResponse(
        data=MessageResponse(
            message="Customer deleted successfully."
        )
    )