import asyncio
import logging
import queue
import threading

from core.market.exchange.api.exchange import Exchange


class ExchangeManager:
    """
    Main driver logic for the system. We run the exchange in one thread,
    and the profiles each run in seperate threads. The agent to exchange
    communication is handled by a thread-safe Queue.
    """
    def __init__(self, sessionId, socket):
        self.exchange = Exchange(id=sessionId, socket=socket)
        self.agents = []# = AgentFactory.create_agent('./profiles/RandomAgent.ini')
        # Queue to manage events between profiles and the exchange
        self.event_queue = queue.Queue()
        self.exchange_thread = threading.Thread(target=self.exchange.run, args=(self.event_queue,))
        self.agent_threads = []

    def start(self):
        self.exchange_thread.start()

    def add_agent(self, agent):
        self.agents.append(agent)
        self.agent_threads.append(threading.Thread(target=agent.run, args=(self.event_queue,)))
        self.agent_threads[-1].start()
        print(f'Started agent thread for: {agent.name}')

    def add_order(self, order):
        logging.debug("Adding order %s to the event queue", order)
        self.event_queue.put(order)
        logging.debug("Order Queue = %s", self.event_queue)

