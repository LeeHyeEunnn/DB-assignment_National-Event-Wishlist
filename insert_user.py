import sqlite3

DB_NAME = "event_wishlist.db"


def insert_default_user():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 이미 user_id = 1이 있으면 건너뛰기
    cur.execute("SELECT user_id FROM User WHERE user_id = 1")
    row = cur.fetchone()

    if row is None:
        cur.execute(
            "INSERT INTO User (user_id, username, email, password) VALUES (?, ?, ?, ?)",
            (1, "test_user", "test@example.com", None),
        )
        conn.commit()
        print("기본 사용자(user_id=1) 추가 완료")
    else:
        print("user_id=1 이미 존재함")

    conn.close()


if __name__ == "__main__":
    insert_default_user()
