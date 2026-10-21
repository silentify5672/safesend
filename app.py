"""
SafeSend - an AI scam shield for elderly people's payments.

Run it:   python app.py      then open http://127.0.0.1:5000

Pages:
  /           the elder's "Send money" page
  /pay/<id>   the AI verdict + PayPal button
  /status/<id> what happened to a payment (updates by itself)
  /contact    the trusted contact's dashboard (approve or block held payments)
  /settings   names, trusted payees, limits, cooling-off time
"""

import os
import secrets
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()  # must run before importing modules that read .env

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

import db
import paypal_client
from risk_check import ai_provider, check_payment

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(16)
db.init_db()

MAX_AMOUNT = 10000

# Example situations for the demo video. Buttons on the home page fill these in.
DEMO_SCENARIOS = [
    {
        "label": "Normal: pay the hawker",
        "recipient": "Uncle Tan Chicken Rice",
        "amount": "12",
        "reason": "Food",
        "message": "",
    },
    {
        "label": "Scam: fake police",
        "recipient": "Inspector Lim",
        "amount": "2000",
        "reason": "Police said to",
        "message": (
            "This is Inspector Lim from the Singapore Police Force. Your bank account "
            "is linked to money laundering. To protect your savings you must transfer "
            "$2,000 to a safe account now or you will be arrested today. "
            "Do not tell anyone, this investigation is confidential."
        ),
    },
    {
        "label": "Scam: grandson in trouble",
        "recipient": "Grandson (new number)",
        "amount": "800",
        "reason": "Family emergency",
        "message": (
            "Ah Ma it's me, I lost my phone so this is my new number. I'm in trouble, "
            "I had an accident and need $800 urgently for the hospital. "
            "Please don't tell Mum, I'll explain later."
        ),
    },
    {
        "label": "Unsure: online seller deposit",
        "recipient": "Carousell seller",
        "amount": "300",
        "reason": "Buying a phone",
        "message": (
            "Hi, the phone is still available. Many buyers want it, so pay $300 "
            "deposit first to reserve it. I will deliver next week."
        ),
    },
]

STATUS_WORDS = {
    "checked": "Not finished",
    "processing": "Working on it…",
    "sent": "Sent",
    "held": "On hold",
    "blocked": "Blocked, money not sent",
    "cancelled": "Cancelled, money not sent",
    "failed": "Something went wrong",
}


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def _parse_time(value):
    return datetime.fromisoformat(value) if value else None


def seconds_until_release(payment):
    release_at = _parse_time(payment.get("release_at"))
    if not release_at:
        return None
    return max(0, int((release_at - datetime.now(timezone.utc)).total_seconds()))


def nice_wait(seconds):
    if seconds is None:
        return ""
    if seconds >= 3600:
        hours = round(seconds / 3600)
        return f"about {hours} hour{'s' if hours != 1 else ''}"
    if seconds >= 60:
        minutes = round(seconds / 60)
        return f"about {minutes} minute{'s' if minutes != 1 else ''}"
    return f"{seconds} second{'s' if seconds != 1 else ''}"


def load_payment_or_404(payment_id):
    payment = db.get_payment(payment_id)
    if not payment:
        abort(404)
    return payment


@app.template_filter("money")
def money(amount):
    return f"${amount:,.2f}"


@app.context_processor
def shared_template_values():
    return {
        "settings": db.get_settings(),
        "status_words": STATUS_WORDS,
        "nice_wait": nice_wait,
        "paypal_ready": paypal_client.is_configured(),
        "ai_name": ai_provider(),
        "currency": paypal_client.CURRENCY,
    }


# --------------------------------------------------------------------------
# The elder's pages
# --------------------------------------------------------------------------


@app.route("/")
def home():
    return render_template("index.html", scenarios=DEMO_SCENARIOS)


@app.route("/check", methods=["POST"])
def check():
    recipient = request.form.get("recipient", "").strip()[:80]
    reason = request.form.get("reason", "").strip()[:120]
    message = request.form.get("message", "").strip()[:2000]
    try:
        amount = round(float(request.form.get("amount", "").replace(",", "").replace("$", "")), 2)
    except ValueError:
        amount = 0

    if not recipient or amount <= 0 or amount > MAX_AMOUNT:
        flash(f"Please enter who you are paying and an amount between $1 and ${MAX_AMOUNT:,}.")
        return redirect(url_for("home"))

    result = check_payment(recipient, amount, reason, message, db.get_settings())
    payment_id = db.create_payment(recipient, amount, reason, message, result)
    return redirect(url_for("pay", payment_id=payment_id))


@app.route("/pay/<int:payment_id>")
def pay(payment_id):
    payment = load_payment_or_404(payment_id)
    if payment["status"] != "checked":
        return redirect(url_for("status", payment_id=payment_id))
    return render_template(
        "pay.html",
        payment=payment,
        paypal_client_id=os.getenv("PAYPAL_CLIENT_ID", ""),
    )


@app.route("/status/<int:payment_id>")
def status(payment_id):
    payment = load_payment_or_404(payment_id)
    return render_template(
        "status.html", payment=payment, wait_seconds=seconds_until_release(payment)
    )


@app.route("/payments/<int:payment_id>/cancel", methods=["POST"])
def cancel(payment_id):
    payment = load_payment_or_404(payment_id)
    if payment["status"] == "checked":
        db.change_status(payment_id, ["checked"], status="cancelled", decided_by="you", decided_at=db.now_iso())
    elif payment["status"] == "held":
        _void_payment(payment, new_status="cancelled", decided_by="you")
    return redirect(url_for("status", payment_id=payment_id))


@app.route("/payments/<int:payment_id>/confirm", methods=["POST"])
def confirm_after_cooling_off(payment_id):
    """After the cooling-off time, the elder can still choose to send."""
    payment = load_payment_or_404(payment_id)
    if payment["status"] == "held" and seconds_until_release(payment) == 0:
        _capture_payment(payment, decided_by="you, after the cooling-off time")
    else:
        flash("This payment is still in its cooling-off time.")
    return redirect(url_for("status", payment_id=payment_id))


# --------------------------------------------------------------------------
# PayPal button (called by JavaScript on the pay page)
# --------------------------------------------------------------------------


@app.route("/api/payments/<int:payment_id>/order", methods=["POST"])
def api_create_order(payment_id):
    payment = load_payment_or_404(payment_id)
    if payment["status"] != "checked":
        return jsonify(error="This payment has already been handled."), 400
    try:
        # The amount comes from our database, never from the browser,
        # so nobody can change it in the page.
        order_id = paypal_client.create_order(payment_id, payment["amount"], payment["recipient"])
    except Exception as error:
        return jsonify(error=str(error)), 502
    db.update_payment(payment_id, order_id=order_id)
    return jsonify(id=order_id)


@app.route("/api/payments/<int:payment_id>/authorize", methods=["POST"])
def api_authorize(payment_id):
    payment = load_payment_or_404(payment_id)
    order_id = (request.get_json(silent=True) or {}).get("orderID")
    if not order_id or order_id != payment["order_id"]:
        return jsonify(error="That PayPal order does not match this payment."), 400
    if not db.change_status(payment_id, ["checked"], status="processing"):
        return jsonify(redirect=url_for("status", payment_id=payment_id))

    try:
        authorization_id = paypal_client.authorize_order(order_id)
    except Exception as error:
        db.update_payment(payment_id, status="checked")
        return jsonify(error=str(error)), 502

    db.update_payment(payment_id, authorization_id=authorization_id)
    payment = db.get_payment(payment_id)

    if payment["verdict"] == "SAFE":
        db.update_payment(payment_id, status="held")
        _capture_payment(db.get_payment(payment_id), decided_by="SafeSend (looked safe)")
    else:
        minutes = int(float(db.get_settings().get("cooling_minutes") or 1440))
        release_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        db.update_payment(
            payment_id, status="held", release_at=release_at.isoformat(timespec="seconds")
        )

    return jsonify(redirect=url_for("status", payment_id=payment_id))


@app.route("/api/payments/<int:payment_id>")
def api_payment(payment_id):
    """Small status feed so pages can update themselves."""
    payment = load_payment_or_404(payment_id)
    return jsonify(
        status=payment["status"],
        status_words=STATUS_WORDS.get(payment["status"], payment["status"]),
        wait_seconds=seconds_until_release(payment),
    )


# --------------------------------------------------------------------------
# Trusted contact
# --------------------------------------------------------------------------


@app.route("/contact")
def contact():
    held = db.list_payments(["held", "processing"])
    for payment in held:
        payment["wait_seconds"] = seconds_until_release(payment)
    # Payments the elder never finished in PayPal didn't move any money, so skip them.
    history = [p for p in db.list_payments(limit=30) if p["status"] not in ("held", "processing", "checked")]
    return render_template("contact.html", held=held, history=history)


@app.route("/contact/<int:payment_id>/approve", methods=["POST"])
def contact_approve(payment_id):
    payment = load_payment_or_404(payment_id)
    if payment["status"] == "held":
        name = db.get_settings()["contact_name"]
        _capture_payment(payment, decided_by=name)
    return redirect(url_for("contact"))


@app.route("/contact/<int:payment_id>/block", methods=["POST"])
def contact_block(payment_id):
    payment = load_payment_or_404(payment_id)
    if payment["status"] == "held":
        name = db.get_settings()["contact_name"]
        _void_payment(payment, new_status="blocked", decided_by=name)
    return redirect(url_for("contact"))


@app.route("/contact/api/held")
def contact_api_held():
    return jsonify(ids=[p["id"] for p in db.list_payments(["held"])])


@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in db.DEFAULT_SETTINGS}
        try:
            values["safe_limit"] = str(max(0, float(values["safe_limit"] or 100)))
            # PayPal holds are most reliable within 3 days, so keep cooling-off under that.
            values["cooling_minutes"] = str(min(4320, max(1, int(float(values["cooling_minutes"] or 1440)))))
        except ValueError:
            flash("Limit and cooling-off time must be numbers.")
            return redirect(url_for("settings_page"))
        db.save_settings(values)
        flash("Settings saved.")
        return redirect(url_for("settings_page"))
    return render_template("settings.html")


@app.route("/health")
def health():
    """Quick check that the PayPal keys work (handy when setting up)."""
    try:
        paypal_client.get_token()
        paypal_status = "connected"
    except Exception as error:
        paypal_status = f"not connected: {error}"
    return jsonify(paypal=paypal_status, ai=ai_provider() or "not set (safety rules only)")


# --------------------------------------------------------------------------
# Capture (send) and void (cancel)
# --------------------------------------------------------------------------


def _capture_payment(payment, decided_by):
    if not db.change_status(payment["id"], ["held"], status="processing"):
        return
    try:
        capture_id = paypal_client.capture(payment["authorization_id"])
        db.update_payment(
            payment["id"], status="sent", capture_id=capture_id,
            decided_by=decided_by, decided_at=db.now_iso(), note="",
        )
    except Exception as error:
        db.update_payment(payment["id"], status="held", note=f"Could not send: {error}"[:300])
        flash("PayPal could not send this payment. Please try again.")


def _void_payment(payment, new_status, decided_by):
    if not db.change_status(payment["id"], ["held"], status="processing"):
        return
    try:
        paypal_client.void(payment["authorization_id"])
        db.update_payment(
            payment["id"], status=new_status,
            decided_by=decided_by, decided_at=db.now_iso(), note="",
        )
    except Exception as error:
        db.update_payment(payment["id"], status="held", note=f"Could not cancel: {error}"[:300])
        flash("PayPal could not cancel this payment. Please try again.")


@app.errorhandler(404)
def not_found(_error):
    return render_template("message.html", title="Not found", text="That page does not exist."), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1", port=port)
