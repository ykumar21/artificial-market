import configparser
import random

from order import OrderTypes, LimitOrder
from utils import emit_every_x_seconds

class Agent:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Load agent configuration
        self.name = self.config['Agent'].get('name', 'DefaultAgent')
        self.strategy = self.config['Agent'].get('strategy', 'DefaultStrategy')
        self.initial_capital = self.config['Agent'].getfloat('initial_capital', 1000.0)
        self.max_positions = self.config['Agent'].getint('max_positions', 1)
        self.risk_tolerance = self.config['Agent'].getfloat('risk_tolerance', 0.01)

        self.exchangeConn = None

    def display_config(self):
        print(f"Agent Name: {self.name}")
        print(f"Strategy: {self.strategy}")
        print(f"Initial Capital: {self.initial_capital}")
        print(f"Max Positions: {self.max_positions}")
        print(f"Risk Tolerance: {self.risk_tolerance}")


    def connectTo(self, exchange):
        self.exchangeConn = exchange

    def emitOrder(self, order):
        raise NotImplemented("Use the agent sub classes")

class RandomAgent(Agent):
    def __init__(self, config, **kwargs):
        super().__init__(config)
        self.clientId = kwargs.get('clientId')
        self._priceRange = kwargs.get("priceRange", (0,100))


    @emit_every_x_seconds(interval=5)
    def emitOrder(self, orderType=OrderTypes.BUY):
        orderId = random.randint(0, 1000)
        limitPrice = random.randint(*self._priceRange)
        size = 100
        self.exchangeConn.sendOrder(LimitOrder(id=orderId, limit=limitPrice, size=size, buyOrSell=orderType))


class PassiveAgent(Agent):
    def __init__(self, config, **kwargs):
        super().__init__(config)
        raise NotImplemented("Passive agent has not been implemented")


class AgentFactory:
    @staticmethod
    def create_agent(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        agent_type = config.get('Agent', 'type')

        if agent_type == 'RandomAgent':
            return RandomAgent(config_file)
        elif agent_type == 'PassiveAgent':
            return PassiveAgent(config_file)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
