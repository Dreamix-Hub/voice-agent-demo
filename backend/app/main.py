from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.api.v1.router import api_router

app = FastAPI(
    title="AI Voice Agent Platform",
    description="Backend API for AI Receptionist",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(
    api_router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    return {
        "name": "AI Receptionist API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }