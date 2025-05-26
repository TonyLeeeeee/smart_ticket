# smart_ticket/async_client.py
import asyncio
import httpx
from typing import Iterable, List
from .config import settings
from .api_client import Ticket, APIError  # 复用模型 & 异常

class AsyncTicketAPI:
    """
    高并发异步客户端。单例使用（保持连接池），线程安全。
    """
    def __init__(self, token: str | None = None, *, max_conn: int = 20):
        limits = httpx.Limits(max_connections=max_conn,
                              max_keepalive_connections=max_conn)
        self._client = httpx.AsyncClient(
            http2=True,
            limits=limits,
            headers={"Authorization": f"Bearer {token or settings.api_token}"}
        )
        self._base = settings.api_base.rstrip("/")

    async def close(self):
        await self._client.aclose()

    # -------- 单查询 ----------
    async def search(self, event_id: str, date: str) -> List[Ticket]:
        url = f"{self._base}/events/{event_id}/tickets"
        try:
            r = await self._client.get(
                url, params={"date": date}, timeout=settings.request_timeout
            )
        except httpx.RequestError as exc:
            raise APIError(f"Network error: {exc}") from exc

        if r.status_code != 200:
            raise APIError(f"{url} -> {r.status_code}: {r.text}")
        return [Ticket(**t) for t in r.json()["tickets"]]

    # -------- 批量并发 ----------
    async def batch_search(
        self, tasks: Iterable[tuple[str, str]]
    ) -> list[list[Ticket] | APIError]:
        async def _one(eid, d):
            try:
                return await self.search(eid, d)
            except APIError as e:
                return e

        coros = [_one(eid, d) for eid, d in tasks]
        return await asyncio.gather(*coros)
