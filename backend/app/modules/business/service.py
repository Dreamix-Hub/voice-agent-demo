from sqlalchemy.orm import Session

from app.common.exceptions import (
    BusinessAlreadyExistsError,
    BusinessNotFoundError,
)
from app.modules.business.models import Business
from app.modules.business.repository import BusinessRepository
from app.modules.business.schemas import (
    BusinessCreate,
    BusinessUpdate,
)


class BusinessService:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def create_business(
        self,
        db: Session,
        data: BusinessCreate,
    ) -> Business:

        if self.repository.get(db):
            raise BusinessAlreadyExistsError()

        business = Business(
            business_name=data.business_name,
            phone=data.phone,
            email=data.email,
            address=data.address,
            timezone=data.timezone,
            opening_time=data.opening_time,
            closing_time=data.closing_time,
            appointment_duration=data.appointment_duration,
            system_prompt=data.system_prompt,
            voice_name=data.voice_name,
            is_active=data.is_active,
        )

        return self.repository.create(db, business)

    def get_business(
        self,
        db: Session,
    ) -> Business:

        business = self.repository.get(db)

        if not business:
            raise BusinessNotFoundError()

        return business

    def update_business(
        self,
        db: Session,
        data: BusinessUpdate,
    ) -> Business:

        business = self.repository.get(db)

        if not business:
            raise BusinessNotFoundError()

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(business, field, value)

        return self.repository.update(db, business)