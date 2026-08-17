#!/usr/bin/env python3
"""
Flask Backend API for Price Predictor
Integrates with Jugraj's React UI for AI-Enabled Price Intelligence
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
CORS(app)

# Sample data endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/commodities', methods=['GET'])
def get_commodities():
    commodities = ["Onion", "Tomato", "Wheat", "Rice (Paddy)", "Potato", "Tur Dal (Arhar)", "Soybean", "Sugarcane"]
    return jsonify({"commodities": commodities})

@app.route('/api/predict', methods=['POST'])
def predict_price():
    """
    Price prediction endpoint
    Expects: {
        "commodity": "string",
        "current_price": float,
        "rainfall": float,
        "temperature": float,
        "demand": float
    }
    """
    try:
        data = request.get_json()
        
        # Simple prediction logic (replace with ML model)
        base_price = data.get('current_price', 2000)
        rainfall = data.get('rainfall', 60)
        temperature = data.get('temperature', 25)
        demand = data.get('demand', 500)
        
        # Calculate prediction
        rain_effect = (rainfall - 60) / 100 * -4
        temp_effect = (temperature - 25) / 100 * 2
        demand_effect = (demand - 500) / 500 * 3
        
        change_pct = rain_effect + temp_effect + demand_effect
        predicted_price = base_price * (1 + change_pct / 100)
        confidence = np.random.randint(75, 96)
        
        return jsonify({
            "commodity": data.get('commodity'),
            "current_price": base_price,
            "predicted_price": round(predicted_price, 2),
            "change_percent": round(change_pct, 2),
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/price-history', methods=['GET'])
def price_history():
    """
    Get historical price data for a commodity
    """
    days = request.args.get('days', 30, type=int)
    commodity = request.args.get('commodity', 'Wheat')
    
    history = []
    base_price = 2400
    for i in range(days):
        price = base_price + np.random.randint(-100, 100)
        history.append({
            "day": i + 1,
            "date": (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d'),
            "price": price
        })
    
    return jsonify({"commodity": commodity, "history": history})

@app.route('/api/buffer-stock', methods=['GET'])
def buffer_stock():
    """
    Get buffer stock recommendations
    """
    return jsonify({
        "current_stock": 3200,
        "recommended_release": 500,
        "recommendation": "Maintain current stock levels",
        "risk_level": "Normal"
    })

if __name__ == '__main__':
    print("\n🚀 Price Predictor Backend API starting...")
    print("🔗 Connect from http://localhost:3000")
    print("📊 API docs at http://localhost:5000/api")
    app.run(debug=True, port=5000, host='0.0.0.0')
