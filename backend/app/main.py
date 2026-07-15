from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.api.v1.router import api_router
from app.core import settings

from app.core.logger import logger
from app.core.lifespan import lifespan
from app.middlewares.logging import logging_middleware

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for AI Receptionist",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

register_exception_handlers(app)

app.middleware("http")(logging_middleware)

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