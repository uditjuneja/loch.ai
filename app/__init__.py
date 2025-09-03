from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

from app.resources import PnL, Portfolio, Trade

api.add_resource(Trade, "/trade")
api.add_resource(Portfolio, "/portfolio")
api.add_resource(PnL, "/pnl")
