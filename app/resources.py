from flask_restful import Resource, reqparse

from app.database import *
from app.models import *

# Hardcoded latest prices
LATEST_PRICES = {Symbol.BTC: 140000, Symbol.ETH: 4000}


class Trade(Resource):
    def __init__(self):
        super().__init__()

        self.trade_parser = reqparse.RequestParser()
        self.trade_parser.add_argument("id", type=int, required=False, help="Trade ID required" )
        self.trade_parser.add_argument("symbol", type=str, required=True, help="Symbol required")
        self.trade_parser.add_argument(
            "side",
            type=str,
            choices=[s.value for s in Side],
            required=True,
            help="Side must be buy or sell",
        )
        self.trade_parser.add_argument("price", type=float, required=True, help="Price required")
        self.trade_parser.add_argument("quantity", type=float, required=True, help="Quantity required")
        self.trade_parser.add_argument("timestamp", type=str, required=True, help="Timestamp required (ISO8601)")

    def __validate_enums(self, args):
        try:
            Symbol(args["symbol"].upper())
        except ValueError:
            return {"message": f"Invalid symbol: {args['symbol']}"}, 400
        try:
            Side(args["side"].lower())
        except ValueError:
            return {"message": f"Invalid side: {args['side']}"}, 400


    def post(self):
        args = self.trade_parser.parse_args()
        self.__validate_enums(args)

        symbol = Symbol(args["symbol"].upper())
        side = Side(args["side"].lower())

        trade = TradeData(
            id=len(TRADES) + 1,
            symbol=symbol,
            side=side,
            price=args["price"],
            quantity=args["quantity"],
            timestamp=args["timestamp"],
        )
        
        TRADES.append(trade)
        holding = HOLDINGS[symbol]

        if trade.side == Side.BUY:
            holding.quantity += trade.quantity
            holding.total_cost += trade.price * trade.quantity
            holding.trades.append(trade)
        else:  # sell
            sell_qty = trade.quantity
            
            avg_entry = (holding.total_cost / holding.quantity) if holding.quantity else 0

            REALIZED_PNL[symbol] += (trade.price - avg_entry) * sell_qty
            holding.quantity -= sell_qty
            holding.total_cost -= avg_entry * sell_qty
            holding.trades.append(trade)
        return {
            "message": "Trade recorded",
            "trade": trade_data_schema.dump(trade),
        }, 201
    
    def get(self):
        return trades_data_schema.dump(TRADES)



class Portfolio(Resource):
    def get(self):
        result = {}
        for symbol, holding in HOLDINGS.items():
            qty = holding.quantity
            avg_entry = (holding.total_cost / qty) if qty else 0
            result[symbol.value] = holding_schema.dump(
                {
                    "quantity": qty,
                    "average_entry_price": avg_entry,
                    "trades": holding.trades,
                }
            )
        return result


class PnL(Resource):
    def get(self):
        # average cost
        pnl = {}
        for symbol, holding in HOLDINGS.items():
            qty = holding.quantity
            avg_entry = (holding.total_cost / qty) if qty else 0
            latest_price = LATEST_PRICES.get(symbol, 0)
            unrealized = (latest_price - avg_entry) * qty if qty else 0
            pnl[symbol.value] = {
                "realized": REALIZED_PNL[symbol],
                "unrealized": unrealized,
                "latest_price": latest_price,
            }
        return pnl
