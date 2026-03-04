from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS licenses(
        license_key TEXT,
        device_id TEXT,
        expiry TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/activate", methods=["POST"])
def activate():
    data = request.json
    key = data["license_key"]
    device = data["device_id"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT device_id, expiry FROM licenses WHERE license_key=?", (key,))
    row = c.fetchone()

    if not row:
        return jsonify({"status":"invalid key"})

    saved_device, expiry = row

    if expiry != "no":
        if datetime.datetime.now() > datetime.datetime.fromisoformat(expiry):
            return jsonify({"status":"expired"})

    if saved_device is None:
        c.execute("UPDATE licenses SET device_id=? WHERE license_key=?", (device, key))
        conn.commit()
        return jsonify({"status":"activated"})

    if saved_device == device:
        return jsonify({"status":"welcome back"})

    return jsonify({"status":"already used on another device"})

app.run(host="0.0.0.0", port=3000)
