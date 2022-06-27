import sqlite3
import pandas as pd


def connect_to_db(db_name):
    """
    connect to the db provided, if not exists it creates the db
    :param db_name: database file path
    :return: connection object to the sqlite db
    """
    conn = sqlite3.connect(db_name)
    return conn


def get_data_as_df(db_name, table_name):
    """
    read data from provided db as pandas dataframe and returns it
    :param db_name: sqlite db name
    :param table_name: table name from which the data has to be read
    :return: pandas dataframe
    """
    conn = connect_to_db(db_name)
    return pd.read_sql_query("select * from {}".format(table_name), conn)

