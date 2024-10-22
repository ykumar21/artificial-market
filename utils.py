import threading
import time


@staticmethod
def print_bst(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.limitPrice), end = " [")
        order = node.headOrder
        while order is not None:
            print(order.id, end=",")
            order = order.nextOrder
        print("]")
        print_bst(node.leftChild, level + 1, prefix="L--- ")
        print_bst(node.rightChild, level + 1, prefix="R--- ")


def emit_every_x_seconds( interval ):
    def decorator( function ):
        def wrapper( *args, **kwargs ):
            def emit():
                while True:
                    target_time = time.time() + interval
                    function( *args, **kwargs )
                    delta = target_time - time.time()
                    time.sleep(delta)
            thread = threading.Thread( target=emit, daemon=True, )
            thread.start()
        return wrapper
    return decorator
