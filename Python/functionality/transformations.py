from datetime import datetime
import pandas as pd


def add_timestamp_column(df: pd.DataFrame, timestamp_column_name: str) -> pd.DataFrame:
    """
    Adds a column with the current timestamp to the input DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame to augment with a timestamp column.
        timestamp_column_name (str): Name of the new column

    Returns:
        pd.DataFrame: DataFrame with the added timestamp column.
    """
    now = datetime.now()
    df[timestamp_column_name] = now

    return df
