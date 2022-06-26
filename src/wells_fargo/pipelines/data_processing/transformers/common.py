import pandas as pd


def add_file_name_as_col(df: pd.DataFrame, col_name: str, file_name: str):
    """
    adds col_name as a column to the passed dataframe df with value as file_name
    :param df: pandas dataframe
    :param col_name: name of the column that has to be added to df
    :param file_name: name of the file from which the dataframe is loaded
    :return: dataframe with col_name as a column and file_name as value to the column
    """
    df[col_name] = file_name
    return df


def concat_data_frames(
        preprocess_sample_data1: pd.DataFrame,
        preprocess_sample_data2: pd.DataFrame,
        preprocess_sample_data3: pd.DataFrame,
):
    return pd.concat(
        [preprocess_sample_data1, preprocess_sample_data2, preprocess_sample_data3],
        axis=0
    )


