from sqlalchemy.orm import Session

from app.modules.customers.model import Customer
from app.modules.customers.repositories import CustomerRepository
from app.modules.customers.schemas import CustomerCreate
from app.common.exceptions import CustomerAlreadyExistsError

class CustomerService:

    def __init__(self):
        self.repository = CustomerRepository()

    def create_customer(
        self,
        db: Session,
        data: CustomerCreate,
    ) -> Customer:

        existing_customer = self.repository.get_by_phone(
            db,
            data.phone,
        )

        if existing_customer:
            raise CustomerAlreadyExistsError()

        customer = Customer(
            name=data.name,
            phone=data.phone,
            email=data.email,
            notes=data.notes,
        )

        return self.repository.create(
            db,
            customer,
        )