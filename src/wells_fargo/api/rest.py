import os
import re
import pandas as pd
import yaml

from typing import Dict, Any
from wells_fargo.api.base import DataSource
from wells_fargo.pipelines.data_processing.db import sqlite_db


class DBNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg


class RestDataSource(DataSource):
    data_source_name = "REST"
    BASE_DIR = os.path.normpath(os.getcwd() + "/../..")
    conf_path = "/conf/base/parameters.yml"
    PATTERN = r'^(?=.)([+-]?([0-9]*)(\.([0-9]+))?)$'

    def read_conf(self, conf_file) -> Dict:
        """
        read the config file
        :param conf_file: path of config file
        :return: dictionary of params present in config file
        """
        conf = {}
        with open(conf_file, 'r') as stream:
            try:
                conf = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            return conf

    def get_conf(self) -> Dict:
        """
        read config data from /conf/base/parameters.yml file
        :return:
        """
        conf_file_path = RestDataSource.BASE_DIR + RestDataSource.conf_path
        return self.read_conf(conf_file_path)

    def get_products_from_db(self, params) -> pd.DataFrame:
        """
        read db_creds from params and read data from db file present on disk.
        Raise DBNotFoundError if unable to find DB file from the db_path
        :param params: parameters read from /conf/base/parameters.yml file
        :return: pandas dataframe
        """
        if params.get('db_creds', '') and params['db_creds'].get('db_name', '') \
                and params['db_creds'].get('db_path', '') and params['db_creds'].get('table_name', ''):
            db_path = RestDataSource.BASE_DIR + params['db_creds']['db_path']
            if os.path.exists(db_path):
                return sqlite_db.get_data_as_df(
                    db_path,
                    params['db_creds']['table_name']
                )
            raise DBNotFoundError('Db not found in path: {}'.format(
                db_path
            ))
        return pd.DataFrame()

    def read_raw_data(self, params) -> pd.DataFrame:
        if params.get('output_file', '') and params['output_file'].get('file_path', ''):
            file_path = RestDataSource.BASE_DIR + params['output_file']['file_path']
            if os.path.isfile(file_path):
                return pd.read_csv(file_path, index_col=False)
        return pd.DataFrame()

    def get_products(self) -> pd.DataFrame:
        """
        read products from output file and return if present else read products from database
        :return: pandas dataframe
        """
        params = self.get_conf()
        file_df = self.read_raw_data(params)
        if not file_df.empty:
            return file_df
        else:
            return self.get_products_from_db(params)

    def _check_int_or_float(self, value: str):
        '''
        checks if value str contains only int or float.
        valid case: 1, 1.0, -2, -3.4
        invalid: 1a, a, abc, 123a
        :param value:
        :return: int(value) if integer or float(value) if float else str
        '''
        if re.match(RestDataSource.PATTERN, value):
            return int(value) if value.isdigit() else float(value)
        return value

    def filter_data(self, data_df: pd.DataFrame, filter_args: Dict[Any, Any]) -> pd.DataFrame:
        """
        filter data frame based on col_name and its value provided
        :param data_df: pandas dataframe
        :param filter_args: filter arguments to filter
        :return: if filter_args provided filtered_data frame is returned else returns original data frame
        """
        if not filter_args:
            return data_df

        col_name = filter_args['filter_col_name']
        col_val = filter_args['filter_col_val']
        # check if provided col_val is an int or float, this makes sure if the col_name value contains
        # all integers or floats then we have to convert the col_val into int or float for matching
        col_val = self._check_int_or_float(col_val)

        df = data_df.loc[
            data_df[col_name] == col_val
        ]
        return df.reset_index(drop=True)
