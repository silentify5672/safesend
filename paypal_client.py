"""
Everything SafeSend says to PayPal lives in this file.

SafeSend never sends money straight away. It uses PayPal's
"authorize now, capture later" feature:

  1. create_order()      -> make an order with intent AUTHORIZE
  2. authorize_order()   -> after the buyer approves in the PayPal pop-up,
                            the money is HELD (not sent yet)
  3. capture()           -> actually send the held money
     void()              -> cancel the hold, the money never leaves

Docs: https://developer.paypal.com/docs/checkout/standard/customize/authorization
"""

import os
import time
import uuid

import requests

# Sandbox = pretend money. Change to https://api-m.paypal.com only for real money.
PAYPAL_API = os.getenv("PAYPAL_API_BASE", "https://api-m.sandbox.paypal.com")
CURRENCY = os.getenv("CURRENCY", "SGD")  # Singapore dollars; set CURRENCY=USD in .env to switch back
SYMBOLS = {"SGD": "S$", "USD": "US$"}


def money(amount):
    """Format an amount with its currency, e.g. S$1,250.00"""
    return f"{SYMBOLS.get(CURRENCY, CURRENCY + ' ')}{amount:,.2f}"


def money_short(amount):
    """Format without cents, e.g. S$1,250"""
    return f"{SYMBOLS.get(CURRENCY, CURRENCY + ' ')}{amount:,.0f}"

_token_cache = {"token": None, "expires_at": 0}


class PayPalError(Exception):
    """Raised when PayPal says no. The message is safe to show on screen."""


def _client_id():
    return os.getenv("PAYPAL_CLIENT_ID", "")


def _client_secret():
    return os.getenv("PAYPAL_CLIENT_SECRET", "")


def is_configured():
    return bool(_client_id() and _client_secret())


def get_token():
    """Get an access token, re-using the last one until it is about to expire."""
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(_client_id(), _client_secret()),
        data={"grant_type": "client_credentials"},
        timeout=15,
    )
    if response.status_code != 200:
        raise PayPalError(
            f"PayPal rejected the keys (HTTP {response.status_code}). "
            "Check PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in your .env file."
        )
    data = response.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + int(data.get("expires_in", 300))
    return _token_cache["token"]


def _call(method, path, json_body=None, idempotency_key=None):
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }
    if idempotency_key:
        # Makes it safe to retry: PayPal will not capture the same money twice.
        headers["PayPal-Request-Id"] = idempotency_key

    response = requests.request(
        method, f"{PAYPAL_API}{path}", headers=headers, json=json_body, timeout=20
    )
    if response.status_code >= 400:
        try:
            details = response.json()
            issue = (details.get("details") or [{}])[0].get("issue") or details.get("name")
            message = details.get("message", "")
        except ValueError:
            issue, message = "UNKNOWN", response.text[:200]
        raise PayPalError(f"PayPal error {response.status_code}: {issue} {message}".strip())

    if response.status_code == 204 or not response.content:
        return {}
    return response.json()


def create_order(payment_id, amount, recipient):
    """Create an order that will only be AUTHORIZED (held), not paid."""
    body = {
        "intent": "AUTHORIZE",
        "purchase_units": [
            {
                "reference_id": f"safesend-{payment_id}",
                "custom_id": str(payment_id),
                "description": f"SafeSend payment to {recipient}"[:127],
                "amount": {"currency_code": CURRENCY, "value": f"{amount:.2f}"},
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "shipping_preference": "NO_SHIPPING",
                    "user_action": "CONTINUE",
                    "brand_name": "SafeSend",
                }
            }
        },
    }
    order = _call("POST", "/v2/checkout/orders", body, idempotency_key=str(uuid.uuid4()))
    return order["id"]


def authorize_order(order_id):
    """Hold the buyer's money. Returns the authorization id."""
    result = _call(
        "POST",
        f"/v2/checkout/orders/{order_id}/authorize",
        {},
        idempotency_key=f"authorize-{order_id}",
    )
    authorization = result["purchase_units"][0]["payments"]["authorizations"][0]
    if authorization.get("status") not in ("CREATED", "PENDING"):
        raise PayPalError(f"Authorization status was {authorization.get('status')}")
    return authorization["id"]


def capture(authorization_id):
    """Send the held money. Returns the capture id."""
    result = _call(
        "POST",
        f"/v2/payments/authorizations/{authorization_id}/capture",
        {"final_capture": True},
        idempotency_key=f"capture-{authorization_id}",
    )
    status = result.get("status", "")
    if status != "COMPLETED":
        # In the sandbox a payment in a currency the seller doesn't hold can be
        # PENDING until the seller accepts it. The money has still left the buyer.
        reason = (result.get("status_details") or {}).get("reason", "")
        print(f"[SafeSend] Capture status is {status} {reason}".strip())
    return result.get("id", "")


def void(authorization_id):
    """Cancel the hold. The money is released back and never sent."""
    _call(
        "POST",
        f"/v2/payments/authorizations/{authorization_id}/void",
        None,
        idempotency_key=f"void-{authorization_id}",
    )
