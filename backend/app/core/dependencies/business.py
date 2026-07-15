from app.modules.business.repository import BusinessRepository
from app.modules.business.service import BusinessService


def get_business_repository() -> BusinessRepository:
    return BusinessRepository()


def get_business_service() -> BusinessService:
    repository = get_business_repository()
    return BusinessService(repository)