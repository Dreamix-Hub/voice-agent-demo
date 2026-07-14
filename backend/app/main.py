from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.modules.customers.router import router as customer_router
from app.modules.business.router import router as business_router
from app.modules.appointments.router import router as appointment_router

app = FastAPI(
    title="AI Voice Agent Platform",
    description="Backend API for AI Receptionist",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(customer_router)
app.include_router(business_router)
app.include_router(appointment_router)


@app.get("/")
def root():
    return {
        "message": "AI Voice Agent API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }