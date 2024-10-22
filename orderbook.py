import threading

from order import OrderTypes


class Limit:
    """
    Class to represent a limit level in the order book. These limits
    hold a doubly-linked list of orders that have that limit price.
    """
    def __init__(self, **kwargs):
        self.limitPrice = kwargs['limitPrice']
        self.leftChild = None
        self.rightChild = None
        self.headOrder = None
        self.tailOrder = None

    def insertOrder(self, order):
        if self.headOrder is None:
            self.headOrder = order
            self.tailOrder = order
        else:
            self.tailOrder.nextOrder = order
            order.prevOrder = self.tailOrder
            self.tailOrder = order

class Book:
    def __init__(self, **kwargs):
        self.buyTree = None
        self.sellTree = None
        self._highestBidPrice = float('-inf')
        self._lowestAskPrice = float('inf')
        self._lastPrice = 0
        self.__treeLock = threading.Lock()

        self._orders = {}

    @staticmethod
    def insertLimitOrder(root, order):
        """
        Adds the order to the root node
        :param root: Root node
        :param order: Order to be added
        :return:
        """
        if root is None:
            # Create a new level with that limit price
            limitLevel = Limit(limitPrice=order.limit)
            limitLevel.insertOrder(order)
            return limitLevel
        if root.limitPrice == order.limit:
            # Add the order to the current level
            root.insertOrder(order)
        elif root.limitPrice < order.limit:
            # Recur downwards and add to the left side
            root.leftChild = Book.insertLimitOrder(root.leftChild, order)
        else:
            # Recur downwards to the right and add the order
            root.rightChild = Book.insertLimitOrder(root.rightChild, order)
        return root

    def process(self, *orders):
        """
        Adds order to the limit order book
        :param order: Order object
        :return: None
        """
        with self.__treeLock:
            for order in orders:
                self._orders[order.id] = order
                if order.buyOrSell == OrderTypes.BUY:
                    # Try to fulfil the order with the current sell tree. In case
                    # no order is matching, then we add in the tree
                    if not self.matchOffer(order):
                        self.buyTree = Book.insertLimitOrder(self.buyTree, order)
                elif order.buyOrSell == OrderTypes.SELL:
                    if not self.matchOffer(order):
                        self.sellTree = Book.insertLimitOrder(self.sellTree, order)
                else:
                    raise NotImplementedError('Only BUY and SELL are implemented')

    def matchOffer(self, order):
        """
        Tries to match the buy offer with eligible sell orders. A bid and ask
        offer is matched only if the bid price is greater than or equal to the ask
        price. and vice versa
        :param order: Order
        :return: True if the order is matched else False
        """
        limitOrderTree = self.sellTree if order.buyOrSell == OrderTypes.BUY else self.buyTree
        limitLevel = self.getMatchOrderLevel( limitOrderTree, order )
        # If no level is matched then we reach
        # the leaf level
        if limitLevel is None or limitLevel.headOrder is None:
            print(f'Unable to match order {order} with existing order book.')
            return False
        # The oldest sell order is matched first
        matchOrder = limitLevel.headOrder
        print(f'Matching orders: {order} - {matchOrder}')
        # Remove the orders for the book
        del self._orders[order.id]
        del self._orders[matchOrder.id]
        limitLevel.headOrder = matchOrder.nextOrder
        # The matched price is always the sell limit price
        self._lastPrice = matchOrder.limit if matchOrder.buyOrSell is OrderTypes.SELL else order.limit
        if limitLevel.headOrder is not None:
            limitLevel.headOrder.prevOrder = None
        return True

    def getMatchOrderLevel(self, limitOrderTree, order):
        limitLevel = limitOrderTree
        if order.buyOrSell == OrderTypes.BUY:
            while limitLevel is not None and (limitLevel.limitPrice >  order.limit):
                limitLevel = limitLevel.rightChild
        else:
            while limitLevel is not None and (limitLevel.limitPrice < order.limit):
                limitLevel = limitLevel.leftChild
        return limitLevel

    @property
    def bestBid(self):
        with self.__treeLock:
            curNode = self.buyTree
            while curNode is not None and curNode.rightChild is not None:
                curNode = curNode.rightChild
        return curNode.limitPrice if curNode is not None else float('-inf')
    @property
    def bestOffer(self):
        with self.__treeLock:
            curNode = self.sellTree
            while curNode is not None and curNode.leftChild is not None:
                curNode = curNode.leftChild
        return curNode.limitPrice if curNode is not None else float('inf')


