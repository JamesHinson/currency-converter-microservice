import requests

def test_microservice():
    # Define request parameters
    from_currency = "USD"
    to_currency = "EUR"
    amount = 100.0

    # Send request to microservice
    response = requests.get("http://127.0.0.1:5000/convert", params={
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount
    })

    # Display response
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.json())

if __name__ == "__main__":
    test_microservice()
