import os
import logging
from flask import Flask, request, jsonify
from src.ml.model_trainer import ModelTrainer
from src.strategies.mean_reversion import MeanReversionStrategy
from src.risk.risk_manager import RiskManager

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize core components
model_trainer = ModelTrainer()
strategy = MeanReversionStrategy()
risk_manager = RiskManager()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "trading bot healthy"}), 200

@app.route('/api/v1/trade/execute', methods=['POST'])
def execute_trade():
    data = request.get_json()
    symbol = data.get('symbol')
    action = data.get('action')  # buy or sell
    quantity = data.get('quantity')
    
    logger.info(f"Executing trade: {action} {quantity} of {symbol}")
    
    # Risk check
    risk_approved = risk_manager.check_trade(symbol, action, quantity)
    if not risk_approved:
        return jsonify({"error": "Trade rejected by risk manager"}), 403
    
    # Execute trade (placeholder)
    result = {"symbol": symbol, "action": action, "quantity": quantity, "status": "executed", "order_id": "dummy_order_123"}
    
    return jsonify(result), 200

@app.route('/api/v1/market/prices', methods=['GET'])
def get_market_prices():
    symbol = request.args.get('symbol')
    # Placeholder for fetching market data
    return jsonify({"symbol": symbol, "price": 100.0, "timestamp": "2026-05-28T01:00:00Z"}), 200

@app.route('/api/v1/portfolio', methods=['GET'])
def get_portfolio():
    # Placeholder for portfolio data
    return jsonify({
        "total_value": 10000.0,
        "cash": 5000.0,
        "positions": [
            {"symbol": "AAPL", "quantity": 100, "value": 15000.0},
            {"symbol": "GOOGL", "quantity": 50, "value": 8000.0}
        ]
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('BOT_PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=False)