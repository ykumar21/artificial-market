import asyncio
import logging
import threading
import time
import queue

from core.agents.api import AgentFactory
from core.market.exchange.api.exchange import Exchange
from core.market.orders.api.types import OrderDirection

def main():
    centralExchange = Exchange()
    client = AgentFactory.create_agent('agents/profiles/RandomAgent.ini')
    client.display_config()
    client.connectTo( centralExchange )
    client.emitOrder(orderType=OrderDirection.BUY)

    # This is a slow implementation - use for debug purposes only
    centralExchange.plotOrderBook()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    manager = ThreadManager(sessionId=1)
    manager.add_agent(AgentFactory.create_agent('agents/profiles/MarketMakerRandom.ini'))

    manager.start()
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

