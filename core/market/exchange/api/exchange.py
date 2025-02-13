import logging

import queue
from collections import Counter
import json
import numpy as np

from core.market.orders.api.types import OrderDirection
from core.market.orderbook.api.orderbook import OrderBook
from utils import emit_every_x_seconds, print_bst

import asyncio

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class Exchange:
    """
    Abstraction to interact with a particular exchange. Allows for trading of different
    assets in seperate order books for independent trading and price discovery.

    Currently, in the implementation the exchange is following HKEX standards.
    """

    EMPTY_SLEEP_DURATIONS_SECONDS = 1

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        # TODO: Remove the socket connection from Exchange - Not its responsibility
        self.socket = kwargs.get('socket')
        # Mapping from ticker -> order book
        self.assetToOrderBookMap = {}
        self.emitBestBidAndOffer()
        self.emitLastPrice()
        self.emitOrderBook()
        self.orderQueue = None

        logger.debug("Initialised Exchange %s", self.id)

    def run(self, eventQueue):
        asyncio.run(self.eventLoop( eventQueue ))
        logging.debug("Shutting down exchange %s", self.id)

    async def eventLoop(self, orderQueue):
        """
        Main function to run the exchange
        :param orderQueue: Thread safe queue of orders
        :return:
        """
        self.orderQueue = orderQueue
        logger.debug("Starting exchange %s thread", self.id)
        while True:
            logger.debug("Order Queue Size: %s", self.orderQueue.qsize())
            order = await self.orderQueue.get() # Will wait till order is retrieved
            logger.debug("Recieved order %s from order queue.", order)
            tickerSymbol = order.ticker
            # In the current model, each asset has its own order book for two reasons:
            #  - Isolated Liquidity: Execute order on asset without impacting others
            #  - Standard Practice: Independent trading and price discovery
            # The class maintains a order book hashmap containing (Asset, OrderBook) pairs
            if tickerSymbol not in self.assetToOrderBookMap:
                logger.info("Generating order book object for Ticker %s", tickerSymbol)
                self.assetToOrderBookMap[tickerSymbol] = OrderBook()
            self.assetToOrderBookMap[tickerSymbol].process(order) # Add the order to the order book
            orderQueue.task_done()  # Mark the order as processed

    @emit_every_x_seconds(interval=1)
    def emitBestBidAndOffer(self):
        for symbol in self.assetToOrderBookMap:
            best_bid = self.assetToOrderBookMap[symbol].bestBid()
            best_ask = self.assetToOrderBookMap[symbol].bestOffer()
            bbo_update = {
                "best_bid": str(best_bid),
                "best_ask": str(best_ask),
            }
            self.socket.emit('bbo_update', json.dumps(bbo_update))

    @emit_every_x_seconds(interval=1)
    def emitLastPrice(self):
        for symbol in self.assetToOrderBookMap:
            self.socket.emit('last_price', f'{self.assetToOrderBookMap[symbol]._lastPrice}')

    @emit_every_x_seconds(interval=1)
    def emitOrderBook(self):
        for symbol in self.assetToOrderBookMap:
            print_bst(self.assetToOrderBookMap[symbol].buyTree)
            print_bst(self.assetToOrderBookMap[symbol].sellTree)
            bidData = [order.limit for orderId, order in self.assetToOrderBookMap[symbol]._orders.items() if
                       order.buyOrSell is OrderDirection.BUY]
            askData = [order.limit for orderId, order in self.assetToOrderBookMap[symbol]._orders.items() if
                       order.buyOrSell is OrderDirection.SELL]

            self.socket.emit('bids', bidData)
            self.socket.emit('asks', askData)

    @DeprecationWarning
    def plotOrderBook(self, bins=20, title='Histogram', xlabel='Value', ylabel='Frequency', color='blue'):
        """
        Plots a histogram of the given data.
        Args:
            data (list or array-like): The input data to plot.
            bins (int): The number of bins for the histogram.
            title (str): The title of the histogram.
            xlabel (str): The label for the x-axis.
            ylabel (str): The label for the y-axis.
            color (str): The color of the bars in the histogram.
        """
        # Sample data (replace with your actual order book data)
        bidData = [order.limit for orderId, order in self.assetToOrderBookMap._orders.items() if
                   order.buyOrSell is OrderDirection.BUY]
        askData = [order.limit for orderId, order in self.assetToOrderBookMap._orders.items() if
                   order.buyOrSell is OrderDirection.SELL]

        # Print the data for debugging
        print("Bid Data:", bidData)
        print("Ask Data:", askData)

        # Aggregate the bid and ask data
        bid_counts = Counter(bidData)
        ask_counts = Counter(askData)

        # Separate prices and volumes for bids and asks
        bid_prices = list(bid_counts.keys())
        bid_volumes = list(bid_counts.values())
        ask_prices = list(ask_counts.keys())
        ask_volumes = list(ask_counts.values())

        # Create a combined list of prices for x-axis
        all_prices = bid_prices + ask_prices
        all_volumes = bid_volumes +  ask_volumes  # Negative for asks

        # Create indices for the bars
        indices = np.arange(len(all_prices))

        # Set up the bar chart
        plt.figure(figsize=(10, 6))

        # Plot bids
        plt.bar(indices[:len(bid_prices)], bid_volumes, color='green', label='Bids')

        # Plot asks (stacked below zero)
        plt.bar(indices[len(bid_prices):],  ask_volumes, color='red', label='Asks')

        # Set x-ticks to price levels
        plt.xticks(indices, all_prices, rotation=45)

        # Add labels and title
        plt.title('Order OrderBook Depth Chart (Bar Chart)')
        plt.xlabel('Price Level')
        plt.ylabel('Volume')
        plt.axhline(0, color='black', linewidth=0.8)  # Add a line at y=0
        plt.grid(axis='y', alpha=0.75)
        plt.legend()

        # Show the plot
        plt.tight_layout()
        plt.show()


