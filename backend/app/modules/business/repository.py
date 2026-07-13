from sqlalchemy.orm import Session

from app.modules.business.models import Business


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

    def get(self, db: Session) -> Business | None:
        return db.query(Business).first()

    def update(
        self,
        db: Session,
        business: Business,
    ) -> Business:
        db.commit()
        db.refresh(business)
        return business