from pydantic import BaseModel, ConfigDict

from .call import RetellCall
from .enums import RetellWebhookEvent


class RetellWebhook(BaseModel):
    """
    Base webhook payload received from Retell.
    """

    model_config = ConfigDict(
        extra="allow",
    )

    event: RetellWebhookEvent

    call: RetellCall