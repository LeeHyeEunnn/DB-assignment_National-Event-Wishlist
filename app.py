from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3

app = Flask(__name__)

DB_NAME = "event_wishlist.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_current_user_id():
    # 로그인 기능 대신, 임시로 user_id=1 고정
    return 1


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events")
def events():
    user_id = get_current_user_id()

    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    region = request.args.get("region", "").strip()

    conn = get_connection()
    cur = conn.cursor()

    # 지역 목록
    cur.execute("""
        SELECT DISTINCT region
        FROM Event
        WHERE region != ''
            AND region NOT IN ('미정', '인처광역시', '충남')
        ORDER BY region
    """)
    region_rows = cur.fetchall()
    regions = [row[0] for row in region_rows]

    # 이벤트 + 찜 여부
    sql = """
        SELECT
            e.event_id,
            e.event_name,
            e.start_date,
            e.end_date,
            e.region,
            e.place,
            CASE
                WHEN w.user_id IS NULL THEN 'N'
                ELSE 'Y'
            END AS is_favorite
        FROM Event e
        LEFT JOIN Wishlist w
            ON e.event_id = w.event_id
           AND w.user_id = ?
        WHERE 1=1
    """
    params = [user_id]

    if start_date:
        sql += " AND e.start_date >= ?"
        params.append(start_date)

    if end_date:
        sql += " AND e.end_date <= ?"
        params.append(end_date)

    if region:
        sql += " AND e.region = ?"
        params.append(region)

    sql += " ORDER BY e.start_date LIMIT 100"

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    result_count = len(rows)
    print("검색 조건:", start_date, end_date, region, "→ 개수:", result_count)

    return render_template(
        "events.html",
        events=rows,
        start_date=start_date,
        end_date=end_date,
        region=region,
        regions=regions,
        result_count=result_count,
    )
    html = render_template(
        "events.html",
        events=rows,
        start_date=start_date,
        end_date=end_date,
        region=region,
        regions=regions,
        result_count=len(rows),
    )

    response = make_response(html)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response



@app.route("/events/<int:event_id>")
def event_detail(event_id):
    user_id = get_current_user_id()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            e.*,
            CASE
                WHEN w.user_id IS NULL THEN 'N'
                ELSE 'Y'
            END AS is_favorite
        FROM Event e
        LEFT JOIN Wishlist w
            ON e.event_id = w.event_id
           AND w.user_id = ?
        WHERE e.event_id = ?
    """, (user_id, event_id))
    event = cur.fetchone()

    conn.close()

    if event is None:
        return "해당 공연을 찾을 수 없습니다.", 404

    return render_template("event_detail.html", event=event)



@app.route("/wishlist")
def wishlist():
    user_id = get_current_user_id()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT e.event_id, e.event_name, e.start_date, e.end_date,
               e.region, e.place
        FROM Wishlist w
        JOIN Event e ON w.event_id = e.event_id
        WHERE w.user_id = ?
        ORDER BY e.start_date
    """, (user_id,))
    rows = cur.fetchall()

    conn.close()

    return render_template("wishlist.html", events=rows)


@app.route("/wishlist/add/<int:event_id>")
def add_wishlist(event_id):
    user_id = get_current_user_id()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO Wishlist (user_id, event_id) VALUES (?, ?)",
        (user_id, event_id),
    )
    conn.commit()
    conn.close()

    next_url = request.referrer or f"/events/{event_id}"
    return redirect(next_url)


@app.route("/wishlist/remove/<int:event_id>")
def remove_wishlist(event_id):
    user_id = get_current_user_id()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM Wishlist WHERE user_id = ? AND event_id = ?",
        (user_id, event_id),
    )
    conn.commit()
    conn.close()

    next_url = request.referrer or "/wishlist"
    return redirect(next_url)




if __name__ == "__main__":
    app.run(debug=True)
