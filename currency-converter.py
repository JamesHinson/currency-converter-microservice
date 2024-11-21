# Name: James Hinson
# OSU Email: hinsonj@oregonstate.edu
# Course: CS361 - Software Engineering I
# Assignment: Assignment 8
# Due Date: 11/18/2024
# Description: This Flask application provides a currency conversion API by fetching exchange rates from a
#              remote service and returning the converted amount and exchange rate in JSON format.

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
API_KEY = os.getenv('API_KEY')
API_URL = f"https://continentl.com/api/currency-exchange?key={API_KEY}"

@app.route('/convert', methods=['GET'])
def convert_currency():
    """
    Convert currency using live exchange rates.
    """
    try:
        # Get input parameters
        from_currency = request.args.get('from_currency')
        to_currency = request.args.get('to_currency')
        amount = float(request.args.get('amount'))

        # Validate inputs
        if not from_currency or not to_currency or amount <= 0:
            return jsonify({"error": "Invalid input parameters"}), 400

        # Fetch exchange rate from the API
        response = requests.get(API_URL, params={
            "Base": from_currency,
            "Foreign": to_currency,
            "Base_amount": amount
        })

        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch exchange rate: {response.status_code}"}), 500

        # Parse API response
        data = response.json()
        if "exchange_rate" not in data or "converted_amount" not in data:
            return jsonify({"error": "Invalid response from currency API"}), 500

        # Extract data
        exchange_rate = float(data["exchange_rate"])
        converted_amount = round(amount * exchange_rate, 2)

        # Return JSON response
        return jsonify({
            "converted_amount": converted_amount,
            "exchange_rate": exchange_rate,
            "from_currency": from_currency,
            "to_currency": to_currency
        })
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)