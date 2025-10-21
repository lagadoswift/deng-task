from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv
import pandas as pd


def main():
    script_dir = str(os.path.dirname(__file__))
    files_dir = script_dir + "\\data\\"

    df = pd.read_parquet(files_dir + "dataset.parquet")
    print(df.describe())

    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_url = os.getenv("DB_URL")
    db_port = os.getenv("DB_PORT")

    db_link = f"postgresql://{db_user}:{db_password}@{db_url}:{db_port}/homeworks"

    engine = create_engine(db_link)

    inspector = inspect(engine)

    if inspector.has_table("kirillov"):
        print("Table already exists")
    else:
        limited_df = df.head(100)

        limited_df.to_sql(
            name="kirillov",
            con=engine,
            if_exists="fail",
            index=False,
        )

    engine.dispose()


if __name__ == "__main__":
    main()
