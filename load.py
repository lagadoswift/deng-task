import os
import pandas as pd
from sqlalchemy import create_engine


def save_to_parquet(
    df: pd.DataFrame, destination: str, name: str = "data.parquet"
) -> None:
    if not os.path.exists(destination):
        os.makedirs(destination)
    df.to_parquet(destination + name, index=False)


def load_to_db(
    df: pd.DataFrame, destination: str, table_name: str, num_of_rows: int = 100
) -> None:

    engine = create_engine(destination)
    limited_df = df.head(num_of_rows)

    limited_df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
    )

    engine.dispose()
