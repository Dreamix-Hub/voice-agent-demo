from retell import Retell


class RetellWebhookVerifier:

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
    ) -> bool:
        """
        Verifies the webhook signature.
        """

        self.client.verify(
            api_key=self.client.api_key,
            body=payload,
            signature=signature,
        )

        return True