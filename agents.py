import random

from order import OrderTypes, LimitOrder
from utils import emit_every_x_seconds


class RandomAgent:
    def __init__(self, **kwargs):
        self.clientId = kwargs.get('clientId')
        self._exchangeConn = kwargs.get("exchange")
        self._priceRange = kwargs.get("priceRange")

    @property
    def exchangeConn(self):
        return self.exchangeConn

    @emit_every_x_seconds(interval=5)
    def emitOrder(self, orderType=OrderTypes.BUY):
        orderId = random.randint(0, 1000)
        limitPrice = random.randint(*self._priceRange)
        size = 100
        self._exchangeConn.sendOrder(LimitOrder(id=orderId, limit=limitPrice, size=size, buyOrSell=orderType))

