from sqlalchemy.orm import Session

from app.modules.business.models import Business
from uuid import UUID

class BusinessRepository:

    def create(
        self,
        db: Session,
        business: Business,
    ) -> Business:
        db.add(business)
        db.commit()
        db.refresh(business)
        return business

    def get(self, db: Session, business_id: UUID) -> Business | None:
        return db.query(Business).filter(Business.id == business_id).first()

    def update(
        self,
        db: Session,
        business: Business,
    ) -> Business:
        db.commit()
        db.refresh(business)
        return business