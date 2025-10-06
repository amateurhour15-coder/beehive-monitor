import time
import threading
import sqlite3
from flask import Flask, render_template, jsonify

from hx711 import HX711
import board
import busio
import adafruit_bme280

app = Flask(__name__, template_folder="templates")
DB_FILE = "beehive_data.db"

hx1 = HX711(5, 6)
hx2 = HX711(13, 19)
hx3 = HX711(20, 21)
hx4 = HX711(26, 16)

i2c = busio.I2C(board.SCL, board.SDA)
bme_in = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme_out = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)

def setup_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                timestamp TEXT,
                weight REAL,
                weight1 REAL,
                weight2 REAL,
                weight3 REAL,
                weight4 REAL,
                temp_in REAL,
                hum_in REAL,
                temp_out REAL,
                hum_out REAL,
                press_in REAL,
                press_out REAL
            )
        """)

def log_data():
    while True:
        w1 = hx1.get_weight(5)
        w2 = hx2.get_weight(5)
        w3 = hx3.get_weight(5)
        w4 = hx4.get_weight(5)
        total_w = w1 + w2 + w3 + w4
        t_in = bme_in.temperature
        h_in = bme_in.humidity
        p_in = bme_in.pressure
        t_out = bme_out.temperature
        h_out = bme_out.humidity
        p_out = bme_out.pressure
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO samples VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (ts, total_w, w1, w2, w3, w4, t_in, h_in, t_out, h_out, p_in, p_out))
        time.sleep(900)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT * FROM samples ORDER BY timestamp DESC LIMIT 1000").fetchall()
    data = [{
        "timestamp": r[0], "weight": r[1], "weight1": r[2], "weight2": r[3],
        "weight3": r[4], "weight4": r[5], "temp_in": r[6], "hum_in": r[7],
        "temp_out": r[8], "hum_out": r[9], "press_in": r[10], "press_out": r[11]
    } for r in rows[::-1]]
    return jsonify(data)

if __name__ == "__main__":
    setup_db()
    threading.Thread(target=log_data, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
