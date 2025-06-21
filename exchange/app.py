"""Minimal FastAPI application implementing a toy crypto exchange."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path

app = FastAPI(title="Simple Crypto Exchange")

# path to static index.html
INDEX_FILE = Path(__file__).resolve().parent / "static" / "index.html"

# in-memory order book storage
ask_orders = []
bid_orders = []

class Order(BaseModel):
    user: str
    pair: str
    side: str  # 'buy' or 'sell'
    price: float
    amount: float

@app.get("/pairs")
def list_pairs() -> List[str]:
    return ["BTC-USD", "ETH-USD"]

@app.post("/order")
def place_order(order: Order):
    if order.side not in ("buy", "sell"):
        raise HTTPException(status_code=400, detail="side must be 'buy' or 'sell'")
    if order.side == "buy":
        bid_orders.append(order)
    else:
        ask_orders.append(order)
    return {"status": "accepted"}


@app.get("/")
def serve_gui() -> HTMLResponse:
    """Return the minimal exchange GUI."""
    return FileResponse(INDEX_FILE)

@app.get("/orderbook/{pair}")
def get_orderbook(pair: str):
    if pair not in ["BTC-USD", "ETH-USD"]:
        raise HTTPException(status_code=404, detail="pair not supported")
    asks = [o.dict() for o in ask_orders if o.pair == pair]
    bids = [o.dict() for o in bid_orders if o.pair == pair]
    return {"asks": asks, "bids": bids}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
