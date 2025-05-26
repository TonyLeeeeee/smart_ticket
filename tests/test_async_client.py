# tests/test_async_client.py
import pytest, httpx, respx, asyncio
from smart_ticket.async_client import AsyncTicketAPI

@pytest.mark.asyncio
async def test_async_search_ok():
    stub = {"tickets":[{"event_id":"EVT001","date":"2025-10-08",
                        "seat_class":"VIP","price":888.0,"remaining":5}]}

    async with respx.mock:
        respx.get("https://sandbox.ticketplatform.com/v1/events/EVT001/tickets")\
             .mock(return_value=httpx.Response(200, json=stub))

        api = AsyncTicketAPI(token="fake", max_conn=5)
        result = await api.search("EVT001", "2025-10-08")
        await api.close()

    assert result[0].seat_class == "VIP"
