import os
import requests
from flask import Flask
from dotenv import load_dotenv

# Read the secret keys from the .env file
load_dotenv()
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_API = "https://api-m.sandbox.paypal.com"  # sandbox = pretend money

app = Flask(__name__)


def get_paypal_token():
    """Ask PayPal for an access token using our sandbox keys."""
    response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["access_token"]


@app.route("/")
def home():
    try:
        get_paypal_token()
        paypal_status = "PayPal sandbox connected ✅"
    except Exception as error:
        paypal_status = f"PayPal connection failed ❌ ({error})"
    return f"<h1>SafeSend is running</h1><p>{paypal_status}</p>"


if __name__ == "__main__":
    app.run(debug=True)