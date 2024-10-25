import threading

from order import OrderTypes, Order, LimitOrder
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
        self.parent = None

    def insertOrder(self, order):
        if self.headOrder is None:
            self.headOrder = order
            self.tailOrder = order
        else:
            self.tailOrder.nextOrder = order
            order.prevOrder = self.tailOrder
            self.tailOrder = order

    def removeOrder(self, order):
        current = self.headOrder
        while current is not None and current.id != order.id:
            current = current.nextOrder

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

class Book:
    def __init__(self, **kwargs):
        self.buyTree = None
        self.sellTree = None
        self._highestBid = None
        self._lowestAsk = None
        self._lastPrice = 0
        self.__treeLock = threading.Lock()

        self._orders = {}

    def removeBstLevel(self, root, level):
        """
        Removes a level from the binary search tree
        :param level: Level to be removed
        :return: Updated tree root
        """
        if level is None:
            raise Exception("Level is undefined. Cannot remove")

        # Case 1 - No children (leaf node)
        if level.rightChild is None and level.leftChild is None:
            if level.parent:
                if level.parent.leftChild == level:
                    level.parent.leftChild = None
                else:
                    level.parent.rightChild = None
            else:
                # All levels have been removed
                return None
            return

        # Case 2 - Single Child
        if level.leftChild is None or level.rightChild is None:
            childNode = level.leftChild if level.leftChild is not None else level.rightChild
            if level.parent:
                if level.parent.leftChild == level:
                    level.parent.leftChild = childNode
                else:
                    level.parent.rightChild = childNode
            if childNode:
                childNode.parent = level.parent
            return

        # Case 3 - Both left and right
        minSuccessor = level
        while minSuccessor.leftChild is not None:
            minSuccessor = minSuccessor.leftChild
        # Swap the nodes
        level.limitPrice = minSuccessor.limitPrice
        level.headOrder = minSuccessor.headOrder
        level.tailOrder = minSuccessor.tailOrder
        # Remove the successor
        self.removeBstLevel(root, minSuccessor)

    def removeLimitOrder(self, root, order):
        """
        Removes a limit order from the book.
        :param root: Node to the binary search tree
        :param order: Order to be removed
        :return: True if the order was removed, False otherwise
        """
        current = root
        while current and current.limitPrice != order.limit:
            if current.limitPrice < order.limit:
                current = current.rightChild
            elif current.limitPrice > order.limit:
                current = current.leftChild
        # Remove the node from the current level
        current.removeOrder(order)
        # Update the BBO
        self.updateBestBid()
        self.updateBestOffer()
        # If current level has no orders left we remove it from the bst
        if current.headOrder is None:
            # Remove this level from the binary search tree
            self.removeBstLevel(self.buyTree if order.buyOrSell is OrderTypes.BUY else OrderTypes.SELL, current)
            print(f'Removed Level: {current.limitPrice} as it was empty.')

    def insertLimitOrder(self, root, order):
        """
        Adds the order to the root node
        :param root: Root node
        :param order: Order to be added
        :return: Updated root node with the added order
        """
        # Create a new level with that limit price
        limitLevel = Limit(limitPrice=order.limit, parent=None)
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
                # Curr level is less than the order so the order must
                # be inserted in the right subtree
                current = current.rightChild
            elif current.limitPrice > order.limit:
                # Curr level is more than the order so the order must
                # be inserted in the left subtree
                current = current.leftChild
            else:
                # Add to this level
                current.insertOrder(order)
                return root

        limitLevel.parent = parent

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
                print(f'Matching orders: {order} {self._lowestAsk.headOrder} @ {self._lowestAsk.limitPrice}' )
                self._lastPrice = self._lowestAsk.headOrder.limit
                self.removeLimitOrder(self.sellTree, self._lowestAsk.headOrder)
                return True
        elif order.buyOrSell is OrderTypes.SELL:
            if order.limit <= self._highestBid.limitPrice:
                print(f'Matching orders: {order} {self._highestBid.headOrder} @ {order.limit}')
                self._lastPrice = order.limit
                self.removeLimitOrder(self.buyTree, self._highestBid.headOrder)
                return True
        print(f'Unable to match order {order} with existing order book.')
        return False

    def updateBestOffer(self):
        """
        Updates the best bid offer from the previous best bid in constant time
        :return: New best offer
        """
        # Check if there are any other orders in the current best bid level
        leftChildExists = self._lowestAsk.leftChild is not None
        rightChildExists = self._lowestAsk.rightChild is not None
        if leftChildExists:
            # Recursively get the right-most child node
            current = self._lowestAsk.leftChild
            while current.leftChild:
                current = current.rightChild
            print(f'New best offer: {current}')
            self._lowestAsk = current
        elif rightChildExists:
            current = self._lowestAsk.rightChild
            print(f'New best offer: {current}')
            self._highestBid = current
        else:
            # If both left and right child do not exist then the
            # best bid is the parent node
            current = self._lowestAsk.parent
            print(f'New best offer: {current}')
            self._lowestAsk = current

    def updateBestBid(self):
        """
        Updates the best bid offer from the previous best bid in constant time
        :param prevBestBidOrder: Previous best bid
        :return: New best bid
        """
        # Check if there are any other orders in the current best bid level
        leftChildExists = self._highestBid.leftChild is not None
        rightChildExists = self._highestBid.rightChild is not None
        if rightChildExists:
            # Recursively get the right-most child node
            current = self._highestBid.rightChild
            while current.rightChild:
                current = current.rightChild
            print(f'New best bid: {current}')
            self._highestBid = current
        elif leftChildExists:
            current = self._highestBid.leftChild
            print(f'New best bid: {current}')
            self._highestBid = current
        else:
            # If both left and right child do not exist then the
            # best bid is the parent node
            current = self._highestBid.parent
            print(f'New best bid: {current}')
            self._highestBid = current

    def bestBid(self):
        return self._highestBid.headOrder if self._highestBid is not None else -1

    def bestOffer(self):
        return self._lowestAsk.headOrder if self._lowestAsk is not None else -1

