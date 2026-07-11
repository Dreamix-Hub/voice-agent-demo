from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.modules.customers.router import router as customer_router

app = FastAPI(
    title="AI Voice Agent API",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(customer_router)


@app.get("/")
def root():
    return {
        "message": "AI Voice Agent API is running."
    }