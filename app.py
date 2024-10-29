import random
from crypt import methods

from flask import Flask, jsonify, request
from flask_cors import CORS


from agents import AgentFactory
from main import ThreadManager

from flask_socketio import SocketIO, emit

from order import LimitOrder, OrderTypes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Dictionary to store exchanges by ID
sessionManagers = { }

@app.route("/subscribe", methods=['POST'])
def subscribe():
    """
    Subscribes to an exchange with the given session id
    :return:
    """
    exchange_id = request.json.get("exchange_id")
    if exchange_id not in sessionManagers:
        return jsonify({"error": "Invalid exchange id"}), 400
    # Create and add the agent
    return jsonify({"success": True}), 200

@app.route('/init', methods=['POST'])
def initialize_exchange():
    exchange_id = request.json.get("exchange_id")
    if not exchange_id:
        return jsonify({"error": "Exchange ID is required."}), 400
    if exchange_id in sessionManagers:
        return jsonify({"error": "Exchange ID already exists."}), 400
    # Create a new session manage with an empty order book
    manager = ThreadManager(sessionId=exchange_id, socket=socketio)
    sessionManagers[exchange_id] = manager
    sessionManagers[exchange_id].start()
    return jsonify({"message": f'Exchange {exchange_id} started', "exchange_id": exchange_id }), 200
@app.route('/create_limit_order', methods=['POST'])
def create_limit_order():
    print(sessionManagers)
    data = request.json  # Get JSON data from the request
    # Validate the input data
    required_fields = ['side', 'size', 'ticker', 'price']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a LimitOrder object using the received data
    print(data['side'])
    order = LimitOrder(
        id=random.randint(100000, 999999),
        buyOrSell=OrderTypes.BUY if data['side'] == 'buy' else OrderTypes.SELL,
        size=data['size'],
        ticker=data['ticker'],
        limit=data['price']
    )
    sessionManagers['1'].add_order(order)
    return jsonify({"message": f'Limit order {order.id} created'}), 200



# Run the app
if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True, allow_unsafe_werkzeug=True)