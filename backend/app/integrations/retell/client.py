from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class RetellClient:
    """
    Client for communicating with the Retell REST API.
    """

    BASE_URL = "https://api.retellai.com"

    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {settings.RETELL_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def close(self) -> None:
        self._client.close()

    def get(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = self._client.get(
            endpoint,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def post(
        self,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = self._client.post(
            endpoint,
            json=json,
        )
        response.raise_for_status()
        return response.json()

    def patch(
        self,
        endpoint: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = self._client.patch(
            endpoint,
            json=json,
        )
        response.raise_for_status()
        return response.json()

    def delete(
        self,
        endpoint: str,
    ) -> dict[str, Any]:
        response = self._client.delete(endpoint)
        response.raise_for_status()

        if response.content:
            return response.json()

        return {}

    # ---------------------------------------------------------------------
    # Calls
    # ---------------------------------------------------------------------

    def get_call(
        self,
        call_id: str,
    ) -> dict[str, Any]:
        return self.get(
            f"/v2/get-call/{call_id}",
        )

    def list_calls(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        return self.get(
            "/v2/list-calls",
            params={
                "limit": limit,
                "offset": offset,
            },
        )

    # ---------------------------------------------------------------------
    # Agents
    # ---------------------------------------------------------------------

    def get_agent(
        self,
        agent_id: str,
    ) -> dict[str, Any]:
        return self.get(
            f"/v2/get-agent/{agent_id}",
        )

    def list_agents(self) -> dict[str, Any]:
        return self.get(
            "/v2/list-agents",
        )