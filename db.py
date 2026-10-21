"""
A tiny SQLite database. It is one file (instance/safesend.db) and needs no setup.

Payment statuses:
  checked    - AI check done, waiting for the elder to approve in PayPal
  sent       - money captured (sent)
  held       - money authorized (held), waiting for the trusted contact or cooling-off
  blocked    - trusted contact blocked it, hold voided, money never sent
  cancelled  - the elder cancelled it themselves
  failed     - something went wrong with PayPal
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("DATABASE_PATH", os.path.join("instance", "safesend.db"))

DEFAULT_SETTINGS = {
    "elder_name": "Ah Ma",
    "contact_name": "Mei Ling (granddaughter)",
    "trusted_payees": "Uncle Tan Chicken Rice, NTUC FairPrice, SP Group, Dr Lim Clinic",
    "safe_limit": "100",
    "cooling_minutes": os.getenv("COOLING_OFF_MINUTES", "1440"),
}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at       TEXT NOT NULL,
                recipient        TEXT NOT NULL,
                amount           REAL NOT NULL,
                reason           TEXT,
                message          TEXT,
                verdict          TEXT NOT NULL,
                reasons          TEXT NOT NULL,
                tip              TEXT,
                source           TEXT,
                status           TEXT NOT NULL DEFAULT 'checked',
                order_id         TEXT,
                authorization_id TEXT,
                capture_id       TEXT,
                release_at       TEXT,
                decided_by       TEXT,
                decided_at       TEXT,
                note             TEXT
            );
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        for key, value in DEFAULT_SETTINGS.items():
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, value))


def get_settings():
    with connect() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    settings = dict(DEFAULT_SETTINGS)
    settings.update({row["key"]: row["value"] for row in rows})
    return settings


def save_settings(values):
    with connect() as conn:
        for key, value in values.items():
            if key in DEFAULT_SETTINGS:
                conn.execute(
                    "INSERT INTO settings (key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                    (key, str(value)),
                )


def _to_dict(row):
    if row is None:
        return None
    data = dict(row)
    data["reasons"] = json.loads(data["reasons"] or "[]")
    # Tips are saved as {"en": ..., "zh": ...}. Older payments saved plain text.
    try:
        tip = json.loads(data["tip"]) if data["tip"] else ""
    except ValueError:
        tip = data["tip"]
    data["tip"] = tip if isinstance(tip, (dict, str)) else ""
    return data


def create_payment(recipient, amount, reason, message, check):
    with connect() as conn:
        cursor = conn.execute(
            """INSERT INTO payments
               (created_at, recipient, amount, reason, message, verdict, reasons, tip, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                now_iso(),
                recipient,
                amount,
                reason,
                message,
                check["verdict"],
                json.dumps(check["reasons"], ensure_ascii=False),
                json.dumps(check.get("tip") or {}, ensure_ascii=False),
                check.get("source", ""),
            ),
        )
        return cursor.lastrowid


def get_payment(payment_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
    return _to_dict(row)


def list_payments(statuses=None, limit=50):
    query = "SELECT * FROM payments"
    params = []
    if statuses:
        query += f" WHERE status IN ({','.join('?' * len(statuses))})"
        params = list(statuses)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    with connect() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_to_dict(row) for row in rows]


def update_payment(payment_id, **fields):
    if not fields:
        return
    columns = ", ".join(f"{key} = ?" for key in fields)
    with connect() as conn:
        conn.execute(
            f"UPDATE payments SET {columns} WHERE id = ?", (*fields.values(), payment_id)
        )


def change_status(payment_id, from_statuses, **fields):
    """Update only if the payment is still in one of from_statuses.
    Returns True if it changed. Stops two people approving AND blocking at once."""
    columns = ", ".join(f"{key} = ?" for key in fields)
    placeholders = ",".join("?" * len(from_statuses))
    with connect() as conn:
        cursor = conn.execute(
            f"UPDATE payments SET {columns} WHERE id = ? AND status IN ({placeholders})",
            (*fields.values(), payment_id, *from_statuses),
        )
        return cursor.rowcount == 1
