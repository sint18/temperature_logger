from flask import Flask, request
import sqlite3
import datetime

app = Flask(__name__)

DATABASE = 'temperature.sqlite3'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/log', methods=['GET'])
def log_data():
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO readings (temperature, humidity) VALUES (?, ?)', (temperature, humidity))
    conn.commit()
    conn.close()
    return 'Data logged successfully'


@app.route('/')
def display_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT temperature, humidity, timestamp FROM readings ORDER BY timestamp DESC')
    data = cursor.fetchall()
    conn.close()
    return '<br>'.join([f"Time: {row[2]}, Temperature: {row[0]}°C, Humidity: {row[1]}%" for row in data])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # --host=0.0.0.0 was added in config
