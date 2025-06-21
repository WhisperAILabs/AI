import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "exchange_app", Path(__file__).resolve().parents[1] / "exchange" / "app.py"
)
exchange_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exchange_app)


def test_list_pairs():
    pairs = exchange_app.list_pairs()
    assert "BTC-USD" in pairs


def test_place_and_get_orderbook():
    # Clear any global state from previous tests
    exchange_app.ask_orders.clear()
    exchange_app.bid_orders.clear()

    order = exchange_app.Order(
        user="alice",
        pair="BTC-USD",
        side="buy",
        price=30000.0,
        amount=0.5,
    )
    exchange_app.place_order(order)
    orderbook = exchange_app.get_orderbook("BTC-USD")
    assert any(o["user"] == "alice" for o in orderbook["bids"])


def test_gui_served():
    resp = exchange_app.serve_gui()
    assert resp.status_code == 200
