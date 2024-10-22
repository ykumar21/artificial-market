import threading
import time

from agents import RandomAgent, AgentFactory
from exchange import Exchange
from order import OrderTypes

def main():
    centralExchange = Exchange()

    client = AgentFactory.create_agent('./agents/RandomAgent.ini')
    client.display_config()
    client.connectTo( centralExchange )
    client.emitOrder(orderType=OrderTypes.BUY)

    # This is a slow implementation - use for debug purposes only
    centralExchange.plotOrderBook()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()