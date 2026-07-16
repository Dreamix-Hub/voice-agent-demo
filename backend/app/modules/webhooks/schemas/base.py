from pydantic import BaseModel, ConfigDict


class RetellWebhookBase(BaseModel):
    """
    Base schema for all Retell webhook events.
    """

    model_config = ConfigDict(extra="allow")

    event: str