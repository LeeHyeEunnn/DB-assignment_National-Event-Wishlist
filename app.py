from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_NAME = "event_wishlist.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 딕셔너리처럼 쓰려고
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events")
def events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_id, event_name, start_date, end_date, region, place
        FROM Event
        ORDER BY start_date
        LIMIT 50
    """)
    rows = cur.fetchall()

    conn.close()
    return render_template("events.html", events=rows)


if __name__ == "__main__":
    app.run(debug=True)
