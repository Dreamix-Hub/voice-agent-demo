from retell import Retell


class RetellWebhookVerifier:
    """
    Verifies incoming Retell webhook requests.
    """

    def __init__(
        self,
        api_key: str,
    ):
        self.client = Retell(
            api_key=api_key,
        )

    def verify(
        self,
        *,
        payload: bytes,
        signature: str,
    ) -> None:
        """
        Raises an exception if the webhook signature is invalid.
        """

        self.client.verify(
            api_key=self.client.api_key,
            body=payload,
            signature=signature,
        )