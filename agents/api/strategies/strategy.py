import random

from core.orders.api.types import LimitOrder, OrderDirection


class Strategy:
    """
    Base class for all strategies. Implement this class and override
    the buy and sell functions to generate signals
    """
    def __init__(self):
        pass

    def buy(self):
        raise NotImplementedError("Use child classes for implementation")

    def sell(self):
        raise NotImplementedError("Use child classes for implementation")


class RandomMarketMaking(Strategy):
    def __init__(self, agent=None):
        super().__init__()
        self.agent = agent

    def connect(self, agent):
        """
        Connects instance of the agent to the strategy
        :return:
        """
        self.agent = agent

    def buy(self):
        """
        Generates a random buy signal and returns order if need to buy.
        :return:
        """
        return [LimitOrder(
            id = random.randint(0, 1000),
            limit = random.randint(*self.agent._priceRange),
            size = 100,
            buyOrSell=OrderDirection.BUY,
            ticker="AAPL"
        )]


    def sell(self):
        """
        Generates a random sell signal and returns order if need to sell.
        :return: List of orders
        """
        return [LimitOrder(
            id=random.randint(0, 1000),
            limit=random.randint(*self.agent._priceRange),
            size=100,
            buyOrSell=OrderDirection.SELL,
            ticker="AAPL"
        )]

class StrategyFactory:
    @staticmethod
    def getStrategy(strategy_name):
        print(strategy_name)
        if strategy_name == "RandomMarketMaking":
            return RandomMarketMaking()
        raise ValueError(f'Strategy {strategy_name} not implemented')
