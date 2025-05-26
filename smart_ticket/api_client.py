from __future__ import annotations
import httpx
from pydantic import BaseModel, Field
from .config import settings

class Ticket(BaseModel):
    event_id: str
    date: str
    seat_class: str
    price: float
    remaining: int = Field(..., ge=0)

class APIError(Exception):
    ...

class TicketAPI:
    _base = settings.api_base.rstrip("/")

    def __init__(self, token: str | None = None, *, timeout: float | None = None):
        self._token = token or settings.api_token
        self._timeout = timeout or settings.request_timeout
        self._headers = {"Authorization": f"Bearer {self._token}"}

    def search(self, event_id: str, date: str) -> list[Ticket]:
        path = f"/events/{event_id}/tickets"
        data = self._get(path, params={"date": date})
        return [Ticket(**t) for t in data["tickets"]]

    def _get(self, path: str, **kwargs) -> dict:
        url = f"{self._base}{path}"
        try:
            r = httpx.get(url, headers=self._headers, timeout=self._timeout, **kwargs)
        except httpx.RequestError as exc:
            raise APIError(f"Network error: {exc}") from exc

        if r.status_code != 200:
            raise APIError(f"{url} -> {r.status_code}: {r.text}")
        return r.json()
