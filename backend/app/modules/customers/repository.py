from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.customers.models import Customer

class CustomerRepository:

    def create(self, db: Session, customer: Customer) -> Customer:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def get_by_id(self, db: Session, customer_id: UUID) -> Customer | None:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    def get_by_phone(self, db: Session, phone: str) -> Customer | None:
        return db.query(Customer).filter(Customer.phone_number == phone).first()

    def get_all(self, db: Session) -> list[Customer]:
        return (
            db.query(Customer)
            .order_by(Customer.created_at.desc())
            .all()
        )

    def update(self, db: Session, customer: Customer) -> Customer:
        db.commit()
        db.refresh(customer)
        return customer

    def delete(self, db: Session, customer: Customer) -> None:
        db.delete(customer)
        db.commit()
    
    def get_by_phone_number(
        self,
        db: Session,
        phone_number: str) -> Customer | None:
        return (
            db.query(Customer)
            .filter(Customer.phone_number == phone_number)
            .first()
    )