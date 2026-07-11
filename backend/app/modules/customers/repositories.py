from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.customers.model import Customer


class CustomerRepository:

    def create(
        self,
        db: Session,
        customer: Customer,
    ) -> Customer:

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    def get_by_id(
        self,
        db: Session,
        customer_id: UUID,
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    def get_by_phone(
        self,
        db: Session,
        phone: str,
    ) -> Customer | None:

        return (
            db.query(Customer)
            .filter(Customer.phone == phone)
            .first()
        )