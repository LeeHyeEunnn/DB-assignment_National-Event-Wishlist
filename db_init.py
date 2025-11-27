import sqlite3

DB_NAME = "event_wishlist.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 공연/행사 정보
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Event (
            event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name  TEXT NOT NULL,
            start_date  TEXT,
            end_date    TEXT,
            region      TEXT,
            place       TEXT,
            category    TEXT,
            host        TEXT,
            fee         TEXT,
            homepage    TEXT
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Event 테이블 생성 완료")
