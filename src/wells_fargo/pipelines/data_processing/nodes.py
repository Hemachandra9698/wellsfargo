"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.1
"""

import pandas as pd

from wells_fargo.pipelines.data_processing.db import sqlite_db
from wells_fargo.pipelines.data_processing.transformers import common as ct
from wells_fargo.pipelines.data_processing.transformers import data1_transformer as dt1
from wells_fargo.pipelines.data_processing.transformers import data2_transformer as dt2
from wells_fargo.pipelines.data_processing.transformers import data3_transformer as dt3
from wells_fargo.pipelines.data_processing.transformers import material_data_transformer as mt


def process_sample_data1(sample_data1: pd.DataFrame, parameters):
    sample_data1 = ct.add_file_name_as_col(
        sample_data1,
        parameters.get('source_col_name', 'source'),
        parameters['data1']['file_name']
    )
    # filter records which have worth column less than 1
    return dt1.filter_rows_with_less_than_a_worth(sample_data1, parameters['data1']['worth'])


def group_and_agg_dataframe(processed_sample_data2: pd.DataFrame, parameters):
    # apply group_by
    df = dt2.group_by(processed_sample_data2, parameters['data2']['group_by'])
    # apply aggregation
    return dt2.aggregate(df, parameters['data2']['aggregation'])


def process_sample_data2(sample_data2: pd.DataFrame, parameters):
    sample_data2 = ct.add_file_name_as_col(
        sample_data2,
        parameters['source_col_name'],
        parameters['data2']['file_name']
    )
    return sample_data2


def process_sample_data3(sample_data3: pd.DataFrame, parameters):
    sample_data3 = ct.add_file_name_as_col(
        sample_data3,
        parameters['source_col_name'],
        parameters['data3']['file_name']
    )
    # re calculate worth values by multiplying worth with material_id column values
    return dt3.re_calculate_worth(sample_data3)


def map_material_id_with_name(
    concat_sample_data_frame: pd.DataFrame,
    material_reference: pd.DataFrame,
    parameters
):
    return mt.map_id_with_name(
        material_reference,
        concat_sample_data_frame,
        parameters['material_data']['merge_on_col']
    )


def store_to_sqlite_db(consolidated_ouput1: pd.DataFrame, parameters):
    conn = sqlite_db.connect_to_db(parameters['db_creds']['db_name'])
    consolidated_ouput1.to_sql(parameters['db_creds']['table_name'], conn, if_exists='replace')
    return consolidated_ouput1
