import os
import random

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

from core.agents.api import AgentFactory
from core.market.exchange.ExchangeManager import ExchangeManager
from core.market.orders.api.types import LimitOrder, OrderDirection

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Dictionary to store exchanges by ID
sessionManagers = { }

# Setup logger
import logging

# Define a custom log format
log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] - %(message)s"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format=log_format,    # Set the log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

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
    manager = ExchangeManager(sessionId=exchange_id, socket=socketio)
    sessionManagers[exchange_id] = manager
    sessionManagers[exchange_id].start()
    return jsonify({"message": f'Exchange {exchange_id} started', "exchange_id": exchange_id }), 200

@app.route('/orders', methods=['POST'])
async def create_limit_order():
    data = request.json  # Get JSON data from the request
    # Validate the input data
    required_fields = ['side', 'size', 'ticker', 'price']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    order = LimitOrder(
        id=random.randint(100000, 999999),
        buyOrSell=OrderDirection.BUY if data['side'] == 'buy' else OrderDirection.SELL,
        size=int(data['size']),
        ticker=data['ticker'],
        limit=float(data['price'])
    )

    sessionManagers['1'].add_order(order)
    return jsonify({"message": f'Limit order {order.id} created'}), 200

@app.route('/profiles', methods=['GET'])
def get_agents():
    agents_folder = 'profiles'  # Ensure this path is correct
    try:
        # List all .ini files in the profiles folder
        agents = [f for f in os.listdir("agents/profiles/") if f.endswith('.ini')]
        return jsonify(agents), 200  # Return the list of profiles as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return an error if something goes wrong

@app.route('/profiles', methods=['POST'])
def create_agent():
    agent_name = request.json.get('agent_name')
    agents_folder = 'profiles'  # Ensure this path is correct
    config_path = os.path.join(agents_folder, agent_name)

    if not os.path.exists(config_path):
        return jsonify({'error': 'Agent config not found'}), 404

    # Here you would create your agent from the loaded config
    agent = AgentFactory.create_agent(config_file=config_path)
    sessionManagers['1'].add_agent(agent)

    return jsonify({'message': f'Agent {agent} created successfully!'}), 201
# Run the app
if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True, allow_unsafe_werkzeug=True)