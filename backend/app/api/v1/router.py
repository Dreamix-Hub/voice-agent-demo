from fastapi import APIRouter

from app.modules.business.router import router as business_router
from app.modules.customers.router import router as customer_router
from app.modules.appointments.router import router as appointment_router

api_router = APIRouter()

api_router.include_router(customer_router)
api_router.include_router(business_router)
api_router.include_router(appointment_router)