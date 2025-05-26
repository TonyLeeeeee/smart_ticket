from fastapi import FastAPI
app = FastAPI(title="Smart Ticket MVP")

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
