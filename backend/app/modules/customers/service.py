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
    def __init__(
        self,
        repository: CustomerRepository,
    ):
        self.repository = repository

    def get_customer_or_raise(
        self,
        db: Session,
        customer_id: UUID,
    ) -> Customer:
        """
        Returns a customer by ID or raises CustomerNotFoundError.
        """

        customer = self.repository.get_by_id(
            db=db,
            customer_id=customer_id,
        )

        if customer is None:
            raise CustomerNotFoundError()

        return customer

    def get_customer(
        self,
        db: Session,
        customer_id: UUID,
    ) -> Customer:
        """
        Returns a customer by ID.
        """

        return self.get_customer_or_raise(
            db=db,
            customer_id=customer_id,
        )

    def get_or_create_by_phone(
        self,
        db: Session,
        *,
        phone_number: str,
    ) -> Customer:
        """
        Returns an existing customer identified by phone number.
        If no customer exists, a new customer record is created.
        """

        customer = self.repository.get_by_phone(
            db=db,
            phone_number=phone_number,
        )

        if customer:
            return customer

        customer = Customer(
            name="Unknown Caller",
            phone_number=phone_number,
        )

        return self.repository.create(
            db=db,
            customer=customer,
        )

    def create_customer(
        self,
        db: Session,
        data: CustomerCreate,
    ) -> Customer:
        """
        Creates a new customer.
        """

        existing_customer = self.repository.get_by_phone(
            db=db,
            phone_number=data.phone,
        )

        if existing_customer:
            raise CustomerAlreadyExistsError()

        customer = Customer(
            name=data.name,
            phone_number=data.phone,
            email=data.email,
            notes=data.notes,
        )

        return self.repository.create(
            db=db,
            customer=customer,
        )

    def list_customers(
        self,
        db: Session,
    ) -> list[Customer]:
        """
        Returns all customers.
        """

        return self.repository.get_all(db)

    def update_customer(
        self,
        db: Session,
        customer_id: UUID,
        data: CustomerUpdate,
    ) -> Customer:
        """
        Updates customer information.
        """

        customer = self.get_customer_or_raise(
            db=db,
            customer_id=customer_id,
        )

        if (
            data.phone
            and data.phone != customer.phone_number
        ):
            existing_customer = self.repository.get_by_phone(
                db=db,
                phone_number=data.phone,
            )

            if (
                existing_customer
                and existing_customer.id != customer.id
            ):
                raise CustomerAlreadyExistsError()

        update_data = data.model_dump(
            exclude_unset=True,
        )

        phone = update_data.pop(
            "phone",
            None,
        )

        if phone is not None:
            customer.phone_number = phone

        for field, value in update_data.items():
            setattr(
                customer,
                field,
                value,
            )

        return self.repository.update(
            db=db,
            customer=customer,
        )

    def delete_customer(
        self,
        db: Session,
        customer_id: UUID,
    ) -> None:
        """
        Deletes a customer.
        """

        customer = self.get_customer_or_raise(
            db=db,
            customer_id=customer_id,
        )

        self.repository.delete(
            db=db,
            customer=customer,
        )