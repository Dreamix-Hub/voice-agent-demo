from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerResponse,
)
from app.modules.customers.services import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

service = CustomerService()


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    return service.create_customer(
        db,
        data,
    )