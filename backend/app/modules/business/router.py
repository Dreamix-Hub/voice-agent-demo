from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.responses import SuccessResponse
from app.database.dependencies import get_db
from app.modules.business.repository import BusinessRepository
from app.modules.business.schemas import (
    BusinessCreate,
    BusinessResponse,
    BusinessUpdate,
)
from app.modules.business.service import BusinessService

router = APIRouter(
    prefix="/business",
    tags=["Business"],
)

repository = BusinessRepository()
service = BusinessService(repository)


@router.post(
    "",
    response_model=SuccessResponse[BusinessResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_business(
    data: BusinessCreate,
    db: Session = Depends(get_db),
):
    business = service.create_business(db, data)

    return SuccessResponse(
        data=BusinessResponse.model_validate(business)
    )


@router.get(
    "",
    response_model=SuccessResponse[BusinessResponse],
)
def get_business(
    db: Session = Depends(get_db),
):
    business = service.get_business(db)

    return SuccessResponse(
        data=BusinessResponse.model_validate(business)
    )


@router.put(
    "",
    response_model=SuccessResponse[BusinessResponse],
)
def update_business(
    data: BusinessUpdate,
    db: Session = Depends(get_db),
):
    business = service.update_business(db, data)

    return SuccessResponse(
        data=BusinessResponse.model_validate(business)
    )