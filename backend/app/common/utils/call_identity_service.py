from app.core.config import settings

from app.modules.retell.schemas import CallStartedRequest


class CallIdentityService:

    def get_phone_number(
        self,
        request: CallStartedRequest,
    ) -> str:

        if settings.ENVIRONMENT == "development":
            if request.call_type == "web_call":
                return settings.DEV_TEST_PHONE_NUMBER

        return request.from_number