import pandas as pd


def change_types(df: pd.DataFrame) -> pd.DataFrame:
    df["Feed_Change_Event"] = df["Feed_Change_Event"].astype(bool)
    df["Catalyst_Replacement"] = df["Catalyst_Replacement"].astype(bool)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df


def fill_nan(df: pd.DataFrame) -> pd.DataFrame:
    # The 'None' string is used here
    df["External_Disturbance_Type"] = df["External_Disturbance_Type"].fillna("None")
    return df
