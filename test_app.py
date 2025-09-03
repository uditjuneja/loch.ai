import json

import pytest

from app import app
from app.database import HOLDINGS, REALIZED_PNL, TRADES


def setup_function():
    TRADES.clear()
    HOLDINGS.clear()
    REALIZED_PNL.clear()


def test_trade_buy_and_portfolio():
    client = app.test_client()
    trade = {
        "symbol": "BTC",
        "side": "buy",
        "price": 30000,
        "quantity": 0.5,
        "timestamp": "2025-09-03T10:00:00Z",
    }
    resp = client.post("/trade", json=trade)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["trade"]["symbol"] == "BTC"
    assert data["trade"]["side"] == "buy"
    assert data["trade"]["price"] == 30000
    assert data["trade"]["quantity"] == 0.5

    # Check portfolio
    pf = client.get("/portfolio").get_json()

    assert "BTC" in pf
    assert pf["BTC"]["quantity"] == 0.5
    assert pf["BTC"]["average_entry_price"] == 30000
    assert pf["BTC"]["trades"][0]["side"] == "buy"
    assert pf["BTC"]["trades"][0]["price"] == 30000


def test_trade_sell_and_pnl():
    client = app.test_client()
    # Buy first
    buy_resp = client.post(
        "/trade",
        json={
            "symbol": "ETH",
            "side": "buy",
            "price": 3900,
            "quantity": 2,
            "timestamp": "2025-09-03T10:10:00Z",
        },
    )
    assert buy_resp.status_code == 201
    # Sell
    sell_resp = client.post(
        "/trade",
        json={
            "symbol": "ETH",
            "side": "sell",
            "price": 4000,
            "quantity": 1,
            "timestamp": "2025-09-03T10:20:00Z",
        },
    )
    assert sell_resp.status_code == 201

    # Check PnL
    pnl = client.get("/pnl").get_json()

    assert "ETH" in pnl
    assert pnl["ETH"]["realized"] == 100
    assert pnl["ETH"]["unrealized"] == 100
    assert pnl["ETH"]["latest_price"] == 4000


def test_trade_multiple_buys_and_sells():
    client = app.test_client()
    # Buy 1 BTC at 35000
    buy1 = client.post(
        "/trade",
        json={
            "symbol": "BTC",
            "side": "buy",
            "price": 135000,
            "quantity": 1,
            "timestamp": "2025-09-03T11:00:00Z",
        },
    )
    assert buy1.status_code == 201
    # Buy 1 BTC at 45000
    buy2 = client.post(
        "/trade",
        json={
            "symbol": "BTC",
            "side": "buy",
            "price": 145000,
            "quantity": 1,
            "timestamp": "2025-09-03T11:10:00Z",
        },
    )
    assert buy2.status_code == 201
    # Sell 1 BTC at 40000
    sell = client.post(
        "/trade",
        json={
            "symbol": "BTC",
            "side": "sell",
            "price": 140000,
            "quantity": 1,
            "timestamp": "2025-09-03T11:20:00Z",
        },
    )
    assert sell.status_code == 201

    # Check portfolio and PnL
    pf = client.get("/portfolio").get_json()
    pnl = client.get("/pnl").get_json()

    assert "BTC" in pf
    assert pf["BTC"]["quantity"] == 1
    assert pf["BTC"]["average_entry_price"] == 140000
    assert len(pf["BTC"]["trades"]) == 3

    assert "BTC" in pnl
    assert pnl["BTC"]["realized"] == 0
    assert pnl["BTC"]["unrealized"] == 0
