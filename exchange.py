import queue
from collections import Counter

import numpy as np

from order import Order, OrderTypes
from orderbook import Book
from utils import emit_every_x_seconds, print_bst

import matplotlib.pyplot as plt

class Exchange:
    def __init__(self):
        self.orderBook = Book()
        self.emitBestBidAndOffer()
        self.emitLastPrice()

    def run(self, orderQueue):
        """
        Main function to run the exchange
        :param orderQueue: Thread safe queue of orders
        :return:
        """
        while True:
            try:
                # Polling for new orders with a timeout
                order = orderQueue.get(timeout=10)
                self.orderBook.process(order) # Add the order to the order book
                orderQueue.task_done()  # Mark the order as processed
            except queue.Empty:
                continue
        print(f'Exiting Exchange Thread...')


    @emit_every_x_seconds(interval=1)
    def emitBestBidAndOffer(self):
        print_bst(self.orderBook.buyTree)
        print_bst(self.orderBook.sellTree)
        print(f'Best BID = {self.orderBook.bestBid()} Best ASK = {self.orderBook.bestOffer()}')

    @emit_every_x_seconds(interval=1)
    def emitLastPrice(self):
        print(f'Last Price [JPMC] = USD{self.orderBook._lastPrice}')

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
                   order.buyOrSell is OrderTypes.BUY]
        askData = [order.limit for orderId, order in self.orderBook._orders.items() if
                   order.buyOrSell is OrderTypes.SELL]

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
        plt.title('Order Book Depth Chart (Bar Chart)')
        plt.xlabel('Price Level')
        plt.ylabel('Volume')
        plt.axhline(0, color='black', linewidth=0.8)  # Add a line at y=0
        plt.grid(axis='y', alpha=0.75)
        plt.legend()

        # Show the plot
        plt.tight_layout()
        plt.show()


