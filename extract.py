import pandas as pd
import os


def get_csv(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    #    print(df.head())
    return df


def save_raw(df: pd.DataFrame, destination: str, name: str = "dataset.csv") -> None:
    if not os.path.exists(destination):
        os.makedirs(destination)

    df.to_csv(destination + name, index=False)
