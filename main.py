import threading
import time
import queue

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

class ThreadManager:
    """
    Main driver logic for the system. We run the exchange in one thread,
    and the agents each run in seperate threads. The agent to exchange
    communication is handled by a thread-safe Queue.
    """
    def __init__(self):

        self.exchange = Exchange()
        self.agent = AgentFactory.create_agent('./agents/RandomAgent.ini')

        # Queue to manage events between agents and the exchange
        self.event_queue = queue.Queue()
        self.exchange_thread = threading.Thread( target=self.exchange.run, args=(self.event_queue,) )
        self.agent_threads = threading.Thread( target=self.agent.run, args=(self.event_queue,) )
    def start(self):
        self.exchange_thread.start()
        self.agent_threads.start()


if __name__ == '__main__':
    manager = ThreadManager()
    manager.start()
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

