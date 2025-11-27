import sqlite3
import pandas as pd

DB_NAME = "event_wishlist.db"
CSV_PATH = "data/전국공연행사정보표준데이터.csv"


def preview_csv():
    print("CSV 경로:", CSV_PATH)

    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
    except FileNotFoundError:
        print("CSV 파일을 찾을 수 없습니다.")
        return

    print("행 개수:", len(df))
    print("컬럼 목록:", list(df.columns))
    print()
    print(df.head(3))


def load_events():
    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
    except FileNotFoundError:
        print("CSV 파일을 찾을 수 없습니다.")
        return

    df = df.fillna("")

    # 홈페이지 컬럼 이름은 살짝 애매해서, '홈페'가 들어간 컬럼을 찾아서 사용
    homepage_col = None
    for col in df.columns:
        if "홈페" in col:
            homepage_col = col
            break

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 기존 데이터 지우고 새로 채우기 (개발용)
    cur.execute("DELETE FROM Event;")

    count = 0

    for _, row in df.iterrows():
        name = str(row["행사명"]).strip()
        if not name:
            continue

        address = row["소재지도로명주소"]
        if isinstance(address, str) and address.strip():
            region = address.split()[0]
        else:
            region = ""

        event_name = name
        start_date = str(row["행사시작일자"]).strip()
        end_date = str(row["행사종료일자"]).strip()
        place = row["장소"].strip() if isinstance(row["장소"], str) else ""

        if isinstance(row["주최기관명"], str) and row["주최기관명"].strip():
            host = row["주최기관명"].strip()
        else:
            host = str(row["주관기관명"]).strip()

        fee = str(row["요금정보"]).strip()

        if homepage_col:
            homepage = str(row[homepage_col]).strip()
        else:
            homepage = ""

        cur.execute(
            """
            INSERT INTO Event (
                event_name, start_date, end_date,
                region, place, category, host, fee, homepage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_name,
                start_date,
                end_date,
                region,
                place,
                "",      # category는 나중에 필요하면 사용
                host,
                fee,
                homepage,
            ),
        )
        count += 1

    conn.commit()
    conn.close()

    print("Event 테이블에 {}개 행 삽입".format(count))


if __name__ == "__main__":
    # preview_csv()  # 필요하면 잠깐 열어서 확인용
    load_events()
