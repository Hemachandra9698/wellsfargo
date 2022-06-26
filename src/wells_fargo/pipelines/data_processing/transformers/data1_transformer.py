import pandas as pd


def filter_rows_with_less_than_a_worth(df: pd.DataFrame, worth):
    return df.loc[df['worth'] > worth]
