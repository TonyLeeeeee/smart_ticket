# smart_ticket/app.py
from fastapi import FastAPI, HTTPException
from smart_ticket.async_client import AsyncTicketAPI, APIError

app = FastAPI(title="Smart Ticket MVP (async)")
api: AsyncTicketAPI | None = None   # 全局变量占位

@app.on_event("startup")
async def on_startup():
    global api
    api = AsyncTicketAPI()

@app.on_event("shutdown")
async def on_shutdown():
    await api.close()               # type: ignore[arg-type]

@app.get("/ping")
async def ping():
    return {"msg": "pong-async"}

@app.get("/demo/{event_id}/{date}")
async def demo(event_id: str, date: str):
    try:
        return await api.search(event_id, date)      # type: ignore[arg-type]
    except APIError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
