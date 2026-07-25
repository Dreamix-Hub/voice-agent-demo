from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GetAvailableSlotsCommand(BaseModel):
    model_config = ConfigDict(frozen=True)

    target_date: date