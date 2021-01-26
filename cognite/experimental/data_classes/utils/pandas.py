import pandas as pd


def dataframe_summarize(dataframe: pd.DataFrame, max_length=1):
    for col in dataframe:
        dataframe[col] = dataframe[col].map(
            lambda v: f"{len(v)} items" if isinstance(v, list) and len(v) > max_length else v
        )
    return dataframe
