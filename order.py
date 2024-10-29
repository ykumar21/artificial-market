import time

class OrderTypes:
    BUY = 1
    SELL = 2

class Order:
    def __init__(self, **kwargs):
        pass

class MarketOrder(Order):
    """
    Class to represent a market order
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs['id']
        self.price = kwargs['price']
        self.size = kwargs['size']
        self.buyOrSell = kwargs['buyOrSell']

class LimitOrder(Order):
    """
    Class to represent a limit order
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.limit = kwargs['limit']
        self.size = kwargs['size']
        self.buyOrSell = kwargs['buyOrSell']
        self.ticker = kwargs['ticker']
        self.eventTime = time.time()
        self.nextOrder = None
        self.prevOrder = None

    def __repr__(self):
        return f'[LimitOrder #{self.id} - { "BUY" if self.buyOrSell == OrderTypes.BUY else "SELL" } {self.size} {self.ticker} @ USD{self.limit}]'

