import pandas as pd


def map_id_with_name(material_df: pd.DataFrame, data_df: pd.DataFrame, merge_on_col):
    material_df = material_df.rename(columns={'id': 'material_id'})
    return pd.merge(data_df, material_df, on=merge_on_col)