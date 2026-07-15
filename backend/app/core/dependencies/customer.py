from app.modules.customers.repository import CustomerRepository
from app.modules.customers.service import CustomerService


def get_customer_repository() -> CustomerRepository:
    return CustomerRepository()


def get_customer_service() -> CustomerService:
    repository = get_customer_repository()
    return CustomerService(repository)