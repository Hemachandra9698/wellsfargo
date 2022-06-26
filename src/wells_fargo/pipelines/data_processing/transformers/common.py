import os

import pandas as pd
from kedro.framework.session import KedroSession


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


def get_kedro_context():
    with KedroSession.create(project_path=os.getcwd()) as session:
        context = session.load_context()
    return context


def get_params():
    context = get_kedro_context()
    return context.params


def get_credentials():
    """
    reads credentials.yml file in the project and returns in dict
    :return: dictionary
    """
    context = get_kedro_context()
    conf_loader = context.config_loader
    return conf_loader.get("credentials*", "credentials*/**")
