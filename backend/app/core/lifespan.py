from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Receptionist API started.")

    yield

    logger.info("AI Receptionist API stopped.")


