import pandas as pd

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


if __name__ == "__main__":
    preview_csv()
