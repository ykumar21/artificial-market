import queue
from collections import Counter
import json
import numpy as np

from core.market.orders.api.types import OrderDirection
from core.market.orderbook.api.orderbook import OrderBook
from utils import emit_every_x_seconds, print_bst

import matplotlib.pyplot as plt

class Exchange:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.socket = kwargs.get('socket')
        # Mapping from ticker -> order book
        self.orderBook = {}
        self.emitBestBidAndOffer()
        self.emitLastPrice()
        self.emitOrderBook()
        self.orderQueue = None

    def run(self, orderQueue):
        """
        Main function to run the exchange
        :param orderQueue: Thread safe queue of orders
        :return:
        """
        self.orderQueue = orderQueue
        while True:
            try:
                # Polling for new orders with a timeout
                order = self.orderQueue.get(timeout=10)
                tickerSymbol = order.ticker
                if tickerSymbol not in self.orderBook:
                    self.orderBook[tickerSymbol] = OrderBook()
                self.orderBook[tickerSymbol].process(order) # Add the order to the order book
                orderQueue.task_done()  # Mark the order as processed

            except queue.Empty:
                continue
        print(f'Exiting Exchange Thread...')

    @emit_every_x_seconds(interval=1)
    def emitBestBidAndOffer(self):
        for symbol in self.orderBook:
            best_bid = self.orderBook[symbol].bestBid()
            best_ask = self.orderBook[symbol].bestOffer()
            bbo_update = {
                "best_bid": str(best_bid),
                "best_ask": str(best_ask),
            }
            self.socket.emit('bbo_update', json.dumps(bbo_update))

    @emit_every_x_seconds(interval=1)
    def emitLastPrice(self):
        for symbol in self.orderBook:
            self.socket.emit('last_price', f'{self.orderBook[symbol]._lastPrice}')

    @emit_every_x_seconds(interval=1)
    def emitOrderBook(self):
        for symbol in self.orderBook:
            print_bst(self.orderBook[symbol].buyTree)
            print_bst(self.orderBook[symbol].sellTree)
            bidData = [order.limit for orderId, order in self.orderBook[symbol]._orders.items() if
                       order.buyOrSell is OrderDirection.BUY]
            askData = [order.limit for orderId, order in self.orderBook[symbol]._orders.items() if
                       order.buyOrSell is OrderDirection.SELL]

            self.socket.emit('bids', bidData)
            self.socket.emit('asks', askData)


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
        bidData = [order.limit for orderId, order in self.orderBook._orders.items() if
                   order.buyOrSell is OrderDirection.BUY]
        askData = [order.limit for orderId, order in self.orderBook._orders.items() if
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


