from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone

from app.common.exceptions import InvalidWebhookSignatureError
from app.core.config import settings


class RetellWebhookVerifier:
    """
    Verifies Retell webhook signatures.
    """

    MAX_TIMESTAMP_AGE = timedelta(minutes=5)

    def verify(
        self,
        *,
        payload: bytes,
        signature_header: str,
    ) -> None:

        if not signature_header:
            raise InvalidWebhookSignatureError()

        values = {}

        for item in signature_header.split(","):
            key, value = item.split("=", maxsplit=1)
            values[key.strip()] = value.strip()

        timestamp = values.get("v")
        signature = values.get("d")

        if not timestamp or not signature:
            raise InvalidWebhookSignatureError()

        timestamp_dt = datetime.fromtimestamp(
            int(timestamp) / 1000,
            tz=timezone.utc,
        )

        if (
            datetime.now(timezone.utc) - timestamp_dt
            > self.MAX_TIMESTAMP_AGE
        ):
            raise InvalidWebhookSignatureError()

        signed_payload = (
            timestamp.encode()
            + b"."
            + payload
        )

        expected_signature = hmac.new(
            settings.RETELL_API_KEY.encode(),
            signed_payload,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            expected_signature,
            signature,
        ):
            raise InvalidWebhookSignatureError()https://docs.retellai.com/features/webhook-overview