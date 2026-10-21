"""
SafeSend - an AI scam shield for elderly people's payments.

Run it:   python app.py      then open http://127.0.0.1:5000

Pages:
  /           the elder's "Send money" page
  /pay/<id>   the AI verdict + PayPal button
  /status/<id> what happened to a payment (updates by itself)
  /contact    the trusted contact's dashboard (approve or block held payments)
  /settings   names, trusted payees, limits, cooling-off time

Every page can be shown in English, Chinese, Malay or Tamil.
The words live in translations.py. Each visitor's choice is remembered
in their own browser, so the elder and the trusted contact can use
different languages.
"""

import os
import secrets
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()  # must run before importing modules that read .env

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, session, url_for

import db
import paypal_client
from risk_check import ai_provider, check_payment
from translations import HTML_LANG, LANG_CODES, LANGUAGES, STRINGS, demo_scenarios, pick, translate

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(16)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)  # remember the language for a year
db.init_db()

MAX_AMOUNT = 10000

# Who decided, saved as short codes so they can be shown in any language.
WHO_AUTO = "auto_safe"
WHO_ELDER = "elder"
WHO_ELDER_AFTER_WAIT = "elder_after_wait"


# --------------------------------------------------------------------------
# Language
# --------------------------------------------------------------------------


def current_lang():
    lang = session.get("lang", "en")
    return lang if lang in LANG_CODES else "en"


def t(key, **values):
    """Translate a key into the visitor's language."""
    return translate(key, current_lang(), **values)


@app.route("/language/<code>")
def set_language(code):
    if code in LANG_CODES:
        session.permanent = True
        session["lang"] = code
    next_page = request.args.get("next", "/")
    # Only go back to a page on this site.
    if not next_page.startswith("/") or next_page.startswith("//"):
        next_page = "/"
    return redirect(next_page)


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
        return t("wait_hour") if hours == 1 else t("wait_hours", n=hours)
    if seconds >= 60:
        minutes = round(seconds / 60)
        return t("wait_minute") if minutes == 1 else t("wait_minutes", n=minutes)
    return t("wait_seconds", n=seconds)


def who_text(value):
    """Turn a saved 'decided_by' into words. Names are shown as they are."""
    codes = {WHO_AUTO: "who_auto_safe", WHO_ELDER: "who_elder", WHO_ELDER_AFTER_WAIT: "who_elder_after_wait"}
    if value in codes:
        return t(codes[value])
    return value or ""


def source_text(value):
    """Turn a saved check source like 'ai:Gemini' into words."""
    code, _, ai = (value or "").partition(":")
    if code in ("ai", "ai_strict", "rules", "rules_down"):
        return t(f"src_{code}", ai=ai)
    return value or ""  # payments saved before translations existed


def message_text(value):
    """Translate a flash message or note if it is a known key."""
    if value in STRINGS:
        return t(value, min=paypal_client.money_short(1), max=paypal_client.money_short(MAX_AMOUNT))
    return value or ""


def load_payment_or_404(payment_id):
    payment = db.get_payment(payment_id)
    if not payment:
        abort(404)
    return payment


@app.template_filter("money")
def money(amount):
    return paypal_client.money(amount)


@app.context_processor
def shared_template_values():
    lang = current_lang()
    here = request.full_path.rstrip("?") if request else "/"
    return {
        "settings": db.get_settings(),
        "t": t,
        "pick": lambda value: pick(value, lang),
        "lang": lang,
        "html_lang": HTML_LANG[lang],
        "languages": LANGUAGES,
        "here": here,
        "nice_wait": nice_wait,
        "who_text": who_text,
        "source_text": source_text,
        "message_text": message_text,
        "paypal_ready": paypal_client.is_configured(),
        "ai_name": ai_provider(),
        "currency": paypal_client.CURRENCY,
        "currency_symbol": paypal_client.SYMBOLS.get(paypal_client.CURRENCY, "$"),
    }


# --------------------------------------------------------------------------
# The elder's pages
# --------------------------------------------------------------------------


@app.route("/")
def home():
    return render_template("index.html", scenarios=demo_scenarios(current_lang()))


@app.route("/check", methods=["POST"])
def check():
    recipient = request.form.get("recipient", "").strip()[:80]
    reason = request.form.get("reason", "").strip()[:120]
    message = request.form.get("message", "").strip()[:2000]
    try:
        amount = round(float(request.form.get("amount", "").replace(",", "").replace("S$", "").replace("$", "")), 2)
    except ValueError:
        amount = 0

    if not recipient or amount <= 0 or amount > MAX_AMOUNT:
        flash("flash_invalid")
        return redirect(url_for("home"))

    result = check_payment(recipient, amount, reason, message, db.get_settings(), current_lang())
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
        db.change_status(payment_id, ["checked"], status="cancelled", decided_by=WHO_ELDER, decided_at=db.now_iso())
    elif payment["status"] == "held":
        _void_payment(payment, new_status="cancelled", decided_by=WHO_ELDER)
    return redirect(url_for("status", payment_id=payment_id))


@app.route("/payments/<int:payment_id>/confirm", methods=["POST"])
def confirm_after_cooling_off(payment_id):
    """After the cooling-off time, the elder can still choose to send."""
    payment = load_payment_or_404(payment_id)
    if payment["status"] == "held" and seconds_until_release(payment) == 0:
        _capture_payment(payment, decided_by=WHO_ELDER_AFTER_WAIT)
    else:
        flash("flash_still_cooling")
    return redirect(url_for("status", payment_id=payment_id))


# --------------------------------------------------------------------------
# PayPal button (called by JavaScript on the pay page)
# --------------------------------------------------------------------------


@app.route("/api/payments/<int:payment_id>/order", methods=["POST"])
def api_create_order(payment_id):
    payment = load_payment_or_404(payment_id)
    if payment["status"] != "checked":
        return jsonify(error=t("api_handled")), 400
    try:
        # The amount comes from our database, never from the browser,
        # so nobody can change it in the page.
        order_id = paypal_client.create_order(payment_id, payment["amount"], payment["recipient"])
    except Exception as error:
        print(f"[SafeSend] PayPal create order failed: {error}")
        return jsonify(error=t("js_error")), 502
    db.update_payment(payment_id, order_id=order_id)
    return jsonify(id=order_id)


@app.route("/api/payments/<int:payment_id>/authorize", methods=["POST"])
def api_authorize(payment_id):
    payment = load_payment_or_404(payment_id)
    order_id = (request.get_json(silent=True) or {}).get("orderID")
    if not order_id or order_id != payment["order_id"]:
        return jsonify(error=t("api_mismatch")), 400
    if not db.change_status(payment_id, ["checked"], status="processing"):
        return jsonify(redirect=url_for("status", payment_id=payment_id))

    try:
        authorization_id = paypal_client.authorize_order(order_id)
    except Exception as error:
        print(f"[SafeSend] PayPal authorize failed: {error}")
        db.update_payment(payment_id, status="checked")
        return jsonify(error=t("js_error")), 502

    db.update_payment(payment_id, authorization_id=authorization_id)
    payment = db.get_payment(payment_id)

    if payment["verdict"] == "SAFE":
        db.update_payment(payment_id, status="held")
        _capture_payment(db.get_payment(payment_id), decided_by=WHO_AUTO)
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
        status_words=t(f"status_{payment['status']}"),
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
            flash("flash_numbers")
            return redirect(url_for("settings_page"))
        db.save_settings(values)
        flash("flash_saved")
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
        print(f"[SafeSend] PayPal capture failed: {error}")
        db.update_payment(payment["id"], status="held", note="note_send_failed")
        flash("flash_send_failed")


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
        print(f"[SafeSend] PayPal void failed: {error}")
        db.update_payment(payment["id"], status="held", note="note_cancel_failed")
        flash("flash_cancel_failed")


@app.errorhandler(404)
def not_found(_error):
    return render_template("message.html", title=t("not_found_title"), text=t("not_found_text")), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1", port=port)
