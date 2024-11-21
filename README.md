# Currency Converter Microservice

## Overview
This microservice provides live currency conversion rates and calculates converted amounts based on input parameters.

## Communication Contract

### Requesting Data
To request data from the microservice, send a GET request to the `/convert` endpoint with the following parameters:
- `from_currency`: The currency code to convert from (e.g., "USD").
- `to_currency`: The currency code to convert to (e.g., "EUR").
- `amount`: The amount to be converted.

Example Request:
```python
import requests

response = requests.get("http://127.0.0.1:5000/convert", params={
    "from_currency": "USD",
    "to_currency": "EUR",
    "amount": 100
})
print(response.json())
```

### Receiving Data
The microservice returns a JSON object with the following fields:
- converted_amount: The converted amount.
- exchange_rate: The exchange rate used for conversion.
- from_currency: The source currency.
- to_currency: The target currency.

### Example Response:
```json
{
  "converted_amount": 85.0,
  "exchange_rate": 0.85,
  "from_currency": "USD",
  "to_currency": "EUR"
}
```