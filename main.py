import threading
import time

from agents import RandomAgent
from exchange import Exchange
from order import OrderTypes

def main():
    centralExchange = Exchange()
    client = RandomAgent(clientId=1, exchange=centralExchange, priceRange=(90,102))
    client.emitOrder(orderType=OrderTypes.BUY)
    client2 = RandomAgent(clientId=2, exchange=centralExchange, priceRange=(98,110))
    client2.emitOrder(orderType=OrderTypes.SELL)

    centralExchange.plotOrderBook()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()