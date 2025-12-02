from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_NAME = "event_wishlist.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events")
def events():
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    region = request.args.get("region", "").strip()

    conn = get_connection()
    cur = conn.cursor()

    # 지역 목록 (드롭다운용)
    cur.execute("""
        SELECT DISTINCT region
        FROM Event
        WHERE region != ''
        ORDER BY region
    """)
    region_rows = cur.fetchall()
    regions = [row[0] for row in region_rows]

    # 기본 쿼리
    sql = """
        SELECT event_id, event_name, start_date, end_date, region, place
        FROM Event
        WHERE 1=1
    """
    params = []

    # 날짜 필터
    if start_date:
        sql += " AND start_date >= ?"
        params.append(start_date)

    if end_date:
        sql += " AND end_date <= ?"
        params.append(end_date)

    # 지역 필터
    if region:
        sql += " AND region = ?"
        params.append(region)

    # 정렬 + 개수 제한
    sql += " ORDER BY start_date LIMIT 100"

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    print("검색 조건:", start_date, end_date, region, "→ 개수:", len(rows))

    return render_template(
        "events.html",
        events=rows,
        start_date=start_date,
        end_date=end_date,
        region=region,
        regions=regions,
    )


@app.route("/events/<int:event_id>")
def event_detail(event_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_id, event_name, start_date, end_date, region, place,
               category, host, fee, homepage
        FROM Event
        WHERE event_id = ?
    """, (event_id,))
    event = cur.fetchone()

    conn.close()

    if event is None:
        return "해당 공연을 찾을 수 없습니다.", 404

    return render_template("event_detail.html", event=event)


if __name__ == "__main__":
    app.run(debug=True)
