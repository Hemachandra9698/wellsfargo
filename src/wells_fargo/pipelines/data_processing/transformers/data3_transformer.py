import pandas as pd


def re_calculate_worth(df: pd.DataFrame):
    df['worth'] = df.worth * df.material_id
    return df
