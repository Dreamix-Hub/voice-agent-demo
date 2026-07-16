from uuid import UUID

from sqlalchemy.orm import Session

from app.common.exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
)
from app.modules.customers.models import Customer
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerUpdate,
)


class CustomerService:

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer_or_raise(
    self,
    db: Session,
    customer_id: UUID,
    ) -> Customer:
        customer = self.repository.get_by_id(db, customer_id)
        if not customer:
            raise CustomerNotFoundError()
        return customer
    
    def create_customer(
        self,
        db: Session,
        data: CustomerCreate,
    ) -> Customer:
        """
        Create a new customer.
        """

        existing_customer = self.repository.get_by_phone(
            db,
            data.phone,
        )

        if existing_customer:
            raise CustomerAlreadyExistsError()

        customer = Customer(
            name=data.name,
            phone_number=data.phone,
            email=data.email,
            notes=data.notes,
        )

        return self.repository.create(db, customer)

    def get_customer(
        self,
        db: Session,
        customer_id: UUID,
    ) -> Customer:
        """
        Get a customer by ID.
        """
        customer = self.get_customer_or_raise(db, customer_id)
        return customer

    def list_customers(
        self,
        db: Session,
    ) -> list[Customer]:
        """
        Return all customers.
        """

        return self.repository.get_all(db)

    def update_customer(
        self,
        db: Session,
        customer_id: UUID,
        data: CustomerUpdate,
    ) -> Customer:
        """
        Update customer information.
        """

        customer = self.repository.get_by_id(
            db,
            customer_id,
        )

        if not customer:
            raise CustomerNotFoundError()

        # Prevent duplicate phone numbers
        if (
            data.phone
            and data.phone != customer.phone_number
        ):
            existing_customer = self.repository.get_by_phone(
                db,
                data.phone,
            )

            if existing_customer:
                raise CustomerAlreadyExistsError()

        # Update only provided fields
        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(customer, field, value)

        return self.repository.update(
            db,
            customer,
        )

    def delete_customer(
        self,
        db: Session,
        customer_id: UUID,
    ) -> None:
        """
        Delete a customer.
        """

        customer = self.repository.get_by_id(
            db,
            customer_id,
        )

        if not customer:
            raise CustomerNotFoundError()

        self.repository.delete(
            db,
            customer,
        )
    
    def get_or_create_by_phone_number(
        self,
        db: Session,
        *,
        phone_number: str) -> Customer:
        """
            Returns an existing customer by phone number or creates
            a new customer if one does not exist.
        """

        customer = self.repository.get_by_phone_number(
            db=db,
            phone_number=phone_number,
        )

        if customer:
            return customer

        customer = Customer(
            name=phone_number,
            phone_number=phone_number,
        )

        return self.repository.create(
            db=db,
            customer=customer,
        )