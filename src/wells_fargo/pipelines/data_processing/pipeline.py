"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.1
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import process_sample_data1, process_sample_data2, process_sample_data3, group_and_agg_dataframe, \
    map_material_id_with_name, store_to_sqlite_db
from wells_fargo.pipelines.data_processing.transformers.common import concat_data_frames


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            name='process_sample_data1_node',
            inputs=['sample_data1', 'parameters'],
            func=process_sample_data1,
            outputs='processed_sample_data1'
        ),
        node(
            name='process_sample_data2_node',
            inputs=['sample_data2', 'parameters'],
            func=process_sample_data2,
            outputs='processed_sample_data2'
        ),
        node(
            name='group_and_agg_processed_sample_data2_node',
            inputs=['processed_sample_data2', 'params:data2'],
            func=group_and_agg_dataframe,
            outputs='data2_aggregation_results'
        ),
        node(
            name='process_sample_data3_node',
            inputs=['sample_data3', 'parameters'],
            func=process_sample_data3,
            outputs='processed_sample_data3'
        ),
        node(
            name='concat_preprocess_dataframes_node',
            inputs=['processed_sample_data1', 'processed_sample_data2', 'processed_sample_data3'],
            func=concat_data_frames,
            outputs='concat_sample_data_frame'
        ),
        node(
            name='merge_preprocess_dataframes_node',
            inputs=['concat_sample_data_frame', 'material_reference', 'parameters'],
            func=map_material_id_with_name,
            outputs='consolidated_output1'
        ),
        node(
            name='store_to_sqlite_node',
            inputs=['consolidated_output1'],
            func=store_to_sqlite_db,
            outputs='df_to_sqlite'
        )
    ])
