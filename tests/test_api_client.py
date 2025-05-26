import httpx                 # ← 新增
import respx
from smart_ticket.api_client import TicketAPI, Ticket


@respx.mock
def test_search_ok():
    api = TicketAPI(token="fake")

    stub = {
        "tickets": [
            {
                "event_id": "EVT001",
                "date": "2025-10-08",
                "seat_class": "VIP",
                "price": 888.0,
                "remaining": 5,
            }
        ]
    }

    route = respx.get(
        "https://sandbox.ticketplatform.com/v1/events/EVT001/tickets"
    ).mock(
        return_value=httpx.Response(200, json=stub)   # ← 用 httpx.Response
    )

    result = api.search("EVT001", "2025-10-08")

    assert route.called
    assert result == [Ticket(**stub["tickets"][0])]

