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

    # 사용자 정보
    cur.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            email       TEXT UNIQUE,
            password    TEXT
        );
    """)

    # 찜 목록 (User - Event 연결)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Wishlist (
            user_id     INTEGER NOT NULL,
            event_id    INTEGER NOT NULL,
            PRIMARY KEY (user_id, event_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (event_id) REFERENCES Event(event_id)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("테이블 생성 완료")
