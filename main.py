import os
import pandas as pd
from dotenv import load_dotenv
from dataclasses import dataclass
from extract import *
from transform import *
from load import *

script_dir = str(os.path.dirname(__file__))
data_dir = script_dir + "\\data\\"


# some of these defaults may be excessive, actually
@dataclass
class Config:
    DB_TABLE_NAME: str
    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 5432
    PARQUET_DIR: str = data_dir + "processed\\"  # note: all folder names must end in \\
    INPUT_FILE: str = data_dir + "raw\\data.csv"
    OUTPUT_DIR: str = data_dir + "raw\\"


def get_env_conf() -> Config:
    load_dotenv()

    return Config(
        DB_TABLE_NAME=os.getenv("DB_TABLE_NAME", "etl_data"),
        DB_URL=os.getenv("DB_URL", "localhost"),
        DB_PORT=os.getenv("DB_PORT", "5432"),
        DB_USER=os.getenv("DB_USER", "user"),
        DB_PASSWORD=os.getenv("DB_PASSWORD", "password"),
        DB_NAME=os.getenv("DB_NAME", "database"),
        INPUT_FILE=os.getenv(
            "INPUT_FILE", data_dir + "raw\\data.csv"
        ),  # in my .env INPUT_FILE is a Google Drive link
        OUTPUT_DIR=os.getenv("OUTPUT_DIR", data_dir + "raw\\"),
    )


def extract_data(config: Config) -> pd.DataFrame:
    # extraction step
    print("Extraction step")
    df = get_csv(config.INPUT_FILE)
    print("Extraction done succesfully")

    ans = input(
        "Type 'yes' to view the head of the dataframe. Leave the query blank to skip. "
    )
    if ans.lower() == "yes":
        print(df.head())

    print("Saving the raw data")
    save_raw(df, config.OUTPUT_DIR, name="data.csv")

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # transformation step
    print("Transformation step")
    print("Changing the types")

    ans = input("Type 'yes' to view the raw types of the columns. ")

    if ans.lower() == "yes":
        print(df.dtypes)
    df = change_types(df)

    ans = input("Type 'yes' to view the changed types of the columns. ")
    if ans.lower() == "yes":
        print(df.dtypes)

    print("Filling empty values")
    df = fill_nan(df)

    return df


def load_data(df: pd.DataFrame, config: Config) -> None:
    # loading step

    print("Uploading the processed data")

    print("Saving to parquet")

    save_to_parquet(df, config.PARQUET_DIR, name="data.parquet")

    # saving to DB

    print("Uploading into the SQL database")
    db_link = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_URL}:{config.DB_PORT}/{config.DB_NAME}"
    rows = input(
        "How many rows do you want to updoad into the database? Only integer values allowed. Default is 100. "
    )
    if not rows:
        rows = 100
    load_to_db(df, db_link, config.DB_TABLE_NAME, num_of_rows=int(rows))


def run_etl(config: Config) -> None:
    df = extract_data(config)
    df = transform_data(df)
    load_data(df, config)


def main() -> None:
    config = get_env_conf()
    run_etl(config)


if __name__ == "__main__":
    main()
