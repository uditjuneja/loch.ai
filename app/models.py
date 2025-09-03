from dataclasses import dataclass
from enum import Enum

from flask_marshmallow import Marshmallow

from app import ma


class Symbol(Enum):
    BTC = "BTC"
    ETH = "ETH"


class Side(Enum):
    BUY = "buy"
    SELL = "sell"


class Holding:
    def __init__(self):
        self.quantity = 0.0
        self.total_cost = 0.0
        self.trades = []

    def to_dict(self):
        return {
            "quantity": self.quantity,
            "total_cost": self.total_cost,
            "trades": self.trades,
        }


@dataclass
class TradeData:
    id: str
    symbol: Symbol
    side: Side
    price: float
    quantity: float
    timestamp: str


class TradeDataSchema(ma.Schema):
    id = ma.Int()
    symbol = ma.Function(lambda obj: obj.symbol.value)
    side = ma.Function(lambda obj: obj.side.value)
    price = ma.Float()
    quantity = ma.Float()
    timestamp = ma.Str()


class HoldingSchema(ma.Schema):
    quantity = ma.Float()
    average_entry_price = ma.Float()
    trades = ma.Nested(TradeDataSchema, many=True)


trade_data_schema = TradeDataSchema()
trades_data_schema = TradeDataSchema(many=True)

holding_schema = HoldingSchema()
