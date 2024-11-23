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

# Hard-coded exchange rates relative to USD
hardcoded_exchange_rates = {
    'USD': {
        'EUR': 0.9439,
        'JPY': 154.54,
        'GBP': 0.7891,
        'AUD': 1.5377,
        'CAD': 1.4021,
        'CHF': 0.8832,
        'CNY': 7.2380,
        'HKD': 7.7839,
        'NZD': 1.6982,
        'SEK': 10.9121
    },
    'EUR': {
        'USD': 1.0594,
        'JPY': 163.77,
        'GBP': 0.8361,
        'AUD': 1.6292,
        'CAD': 1.4870,
        'CHF': 0.9358,
        'CNY': 7.6670,
        'HKD': 8.2390,
        'NZD': 1.8000,
        'SEK': 11.5560
    }
}

# Get API key from environment variables
API_KEY = os.getenv('API_KEY')
API_URL = f"https://continentl.com/api/currency-exchange?key={API_KEY}"


@app.route('/convert', methods=['GET'])
def convert_currency():
    try:
        # Get input parameters
        from_currency = request.args.get('from_currency')
        to_currency = request.args.get('to_currency')
        amount = request.args.get('amount')

        # Validate inputs
        if not from_currency or not to_currency or not amount:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            amount = float(amount)
        except ValueError:
            return jsonify({"error": "Amount must be a number"}), 400

        if amount <= 0:
            return jsonify({"error": "Amount must be greater than zero"}), 400

        # Attempt to fetch exchange rate from API
        try:
            response = requests.get(API_URL, params={"Base": from_currency, "Foreign": to_currency, "Base_amount": amount})
            if response.status_code == 200:
                data = response.json()
                exchange_rate = float(data["exchange_rate"])
            else:
                raise Exception(f"API returned status code {response.status_code}")
        except Exception as e:
            print(f"API error: {e}. Falling back to hardcoded values.")
            # Use hardcoded values if API call fails
            if from_currency in hardcoded_exchange_rates and to_currency in hardcoded_exchange_rates[from_currency]:
                exchange_rate = hardcoded_exchange_rates[from_currency][to_currency]
            elif to_currency in hardcoded_exchange_rates and from_currency in hardcoded_exchange_rates[to_currency]:
                exchange_rate = 1 / hardcoded_exchange_rates[to_currency][from_currency]
            else:
                return jsonify({"error": "Currency pair not supported"}), 400

        # Calculate converted amount
        converted_amount = round(amount * exchange_rate, 2)

        # Return JSON response
        return jsonify({
            "converted_amount": converted_amount,
            "exchange_rate": exchange_rate,
            "from_currency": from_currency,
            "to_currency": to_currency
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000)  
