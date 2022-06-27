"""
This is a pipeline 'data_processing'
generated using Kedro 0.18.1
"""

import pandas as pd

from wells_fargo.pipelines.data_processing.db import sqlite_db
from wells_fargo.pipelines.data_processing.transformers import common as common_transformer
from wells_fargo.pipelines.data_processing.transformers import rest_transformer
from wells_fargo.pipelines.data_processing.transformers import material_data_transformer as material_transformer


def process_sample_data1(sample_data1: pd.DataFrame, parameters):
    """
    processes sample data1 -> adds a source col and file_name from which the data has been read
    as value. Filters rows with less than given 'worth' col value
    :param sample_data1: pandas dataframe
    :param parameters: dict of parameters read from conf/base/parameters/<pipeline-name>.yml
    :return: processed pandas dataframe
    """
    sample_data1 = common_transformer.add_file_name_as_col(
        sample_data1,
        parameters.get('source_col_name', 'source'),
        parameters['data1']['file_name']
    )
    # filter records which have worth column less than 1
    return rest_transformer.filter_rows_with_less_than_a_worth(sample_data1, parameters['data1']['worth'])


def group_and_agg_dataframe(processed_sample_data2: pd.DataFrame, data_param_name):
    """
    groups by given column and applies aggregations provided in conf/base/parameters/<pipeline-name>.yml
    :param processed_sample_data2:
    :param data_param_name:
    :return:
    """
    # apply group_by
    df = rest_transformer.group_by(processed_sample_data2, data_param_name['group_by'])
    # apply aggregation
    return rest_transformer.aggregate(df, data_param_name['aggregation'])


def process_sample_data2(sample_data2: pd.DataFrame, parameters):
    """
    processes sample data2 -> adds a source col and file_name from which the data has been read
    as value.
    :param sample_data2: pandas dataframe
    :param parameters: dict of parameters read from conf/base/parameters/<pipeline-name>.yml
    :return: processed pandas dataframe
    """
    sample_data2 = common_transformer.add_file_name_as_col(
        sample_data2,
        parameters['source_col_name'],
        parameters['data2']['file_name']
    )
    return sample_data2


def process_sample_data3(sample_data3: pd.DataFrame, parameters):
    """
    processes sample data3 -> adds a source col and file_name from which the data has been read
    as value. Also re calculates worth col values by multiplying material_id col with worth col.
    :param sample_data2: pandas dataframe
    :param parameters: dict of parameters read from conf/base/parameters/<pipeline-name>.yml
    :return: processed pandas dataframe
    """
    sample_data3 = common_transformer.add_file_name_as_col(
        sample_data3,
        parameters['source_col_name'],
        parameters['data3']['file_name']
    )
    # re calculate worth values by multiplying worth with material_id column values
    return rest_transformer.re_calculate_worth(sample_data3)


def map_material_id_with_name(
    concat_sample_data_frame: pd.DataFrame,
    material_reference: pd.DataFrame,
    parameters
):
    """
    renames material_reference.csv's Id column to 'material_id' column and then merges
    with dataframe on provided column -> 'merge_on_col'
    :param concat_sample_data_frame: total data frame
    :param material_reference: material_reference csv pandas dataframe
    :param parameters: dict of parameters read from conf/base/parameters/<pipeline-name>.yml
    :return: merged dataframe
    """
    return material_transformer.map_id_with_name(
        material_reference,
        concat_sample_data_frame,
        parameters['material_data']['merge_on_col']
    )


def store_to_sqlite_db(consolidated_ouput1: pd.DataFrame):
    """
    stores dataframe rows into sqlite db by getting credentials from
    dict of parameters read from conf/local/credentials.yml
    :param consolidated_ouput1: final pandas dataframe to be stored into db
    :return: pandas dataframe
    """
    credentials = common_transformer.get_credentials()
    conn = sqlite_db.connect_to_db(credentials['db_creds']['db_name'])
    consolidated_ouput1.to_sql(credentials['db_creds']['table_name'], conn, if_exists='replace', index=False)
    return consolidated_ouput1
