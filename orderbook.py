import threading

from order import OrderTypes
from utils import print_bst


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
        self._highestBid = None
        self._lowestAsk = None
        self._lastPrice = 0
        self.__treeLock = threading.Lock()

        self._orders = {}

    def removeOrder(self, order):
        current = self.headOrder
        while current is not None and current.id != order.id:
            current = current.next

        if current is None:
            raise Exception(f'Order {order} does not exist')

        if current is self.headOrder:
            self.headOrder = current.nextOrder
        else:
            previousOrder = current.prevOrder
            nextOrder = current.nextOrder
            previousOrder.nextOrder = nextOrder
            if nextOrder:
                nextOrder.prevOrder = previousOrder
        print(f'Removed order {order}')
        return True

    def removeLimitOrder(self, root, order):
        """
        Removes a limit order from the book.
        :param root: Node to the binary search tree
        :param order: Order to be removed
        :return: True if the order was removed, False otherwise
        """
        current = root
        while current:
            if current.limitPrice < order.limit:
                current = current.rightChild
            elif current.limitPrice > order.limit:
                current = current.leftChild
            else:
                # Remove the node from the current level
                current.removeOrder(order)

    def insertLimitOrder(self, root, order):
        """
        Adds the order to the root node
        :param root: Root node
        :param order: Order to be added
        :return: Updated root node with the added order
        """
        # Create a new level with that limit price
        limitLevel = Limit(limitPrice=order.limit)
        limitLevel.insertOrder(order)

        # Update the best bid and offers
        if order.buyOrSell is OrderTypes.BUY:
            self._highestBid = limitLevel if self._highestBid is None or order.limit > self._highestBid.limitPrice else self._highestBid
        if order.buyOrSell is OrderTypes.SELL:
            self._lowestAsk = limitLevel if self._lowestAsk is None or order.limit < self._lowestAsk.limitPrice else self._lowestAsk

        if root is None:
            return limitLevel

        current = root
        parent = None
        while current:
            parent = current
            if current.limitPrice < order.limit:
                # Curr level is less than the order so the order
                # must be inserted in the right subtree
                current = current.rightChild
            elif current.limitPrice > order.limit:
                # Curr level is more than the order so the order
                # must be inserted in the left subtree
                current = current.leftChild
            else:
                # Add to this level
                current.insertOrder(order)
                return root

        if parent.limitPrice < order.limit:
            parent.rightChild = limitLevel
        else:
            parent.leftChild = limitLevel

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
                        self.buyTree = self.insertLimitOrder(self.buyTree, order)
                elif order.buyOrSell == OrderTypes.SELL:
                    if not self.matchOffer(order):
                        self.sellTree = self.insertLimitOrder(self.sellTree, order)
                else:
                    raise NotImplementedError('Only BUY and SELL are implemented')

    def should_match(self, limitPrice, orderPrice, is_buy):
        """
        Compares the current limit order book level and checks if the order is eligible for that level
        :param orderPrice:
        :param is_buy:
        :return:
        """
        return (is_buy and limitPrice < orderPrice) or (not is_buy and limitPrice > orderPrice)


    def matchOffer(self, order):
        """
        Tries to match the buy offer with eligible sell orders. A bid and ask
        offer is matched only if the bid price is greater than or equal to the ask
        price. and vice versa
        :param order: Order
        :return: True if the order is matched else False
        """
        if self._highestBid is None or self._lowestAsk is None:
            print(f'Unable to match order {order}')
            return False

        if order.buyOrSell is OrderTypes.BUY:
            if order.limit >= self._lowestAsk.limitPrice:
                print(f'Matching orders: {order} {self._lowestAsk.headOrder}')
                self._lowestAsk.removeOrder(self._lowestAsk.headOrder)
                return True

        elif order.buyOrSell is OrderTypes.SELL:
            if order.limit <= self._highestBid.limitPrice:
                print(f'Matching orders: {order} {self._highestBid.headOrder}')
                self._highestBid.removeOrder(self._highestBid.headOrder)
                return True

        print(f'Unable to match order {order} with existing order book.')
        return False

    def getMatchOrderLevel(self, limitOrderTree, order):
        limitLevel = limitOrderTree
        is_buy = order.buyOrSell == OrderTypes.BUY
        while limitLevel is not None:
            if self.should_match(limitLevel.limitPrice, order.limit, is_buy):
                return limitLevel  # Found a matching level
            # Traverse the tree based on order type
            limitLevel = limitLevel.rightChild if is_buy else limitLevel.leftChild

    def bestBid(self):
        return self._highestBid.headOrder if self._highestBid is not None else -1

    def bestOffer(self):
        return self._lowestAsk.headOrder if self._lowestAsk is not None else -1

