from collections import defaultdict

from app.models import Holding

TRADES = []
HOLDINGS = defaultdict(Holding)
REALIZED_PNL = defaultdict(float)
