import pandas as pd

STRING_AGG = ['first']


def filter_rows_with_less_than_a_worth(df: pd.DataFrame, worth):
    return df.loc[df['worth'] > worth]


def group_by(df: pd.DataFrame, group_by_col):
    return df.groupby(group_by_col)


def aggregate(df: pd.DataFrame, aggregation_dict):
    '''
    aggregation_dict = {'quality': 'first', 'material_id': 'max', 'worth': 'sum'}
    max and sum in the dict are type str, we have to evaluate them into python functions.
    Also skip string aggregations and evaluate remaining
    '''
    for col_name, agg_name in aggregation_dict.items():
        if agg_name not in STRING_AGG:
            aggregation_dict[col_name] = eval(agg_name)

    return df.agg(aggregation_dict)


def re_calculate_worth(df: pd.DataFrame):
    df['worth'] = df.worth * df.material_id
    return df
