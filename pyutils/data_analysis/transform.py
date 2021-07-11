from typing import Callable, Dict, List, Optional, Union
from functools import reduce
import random

import numpy as np
import pandas as pd

from pyutils.date_ops.date_ops import get_current_timestamp_as_integer
from pyutils.general.casing import (
    lcc2sc,
    lcc2ucc,
    sc2lcc,
    sc2ucc,
    ucc2lcc,
    ucc2sc,
)
from pyutils.general.utils import (
    get_indices_for_partitioning,
    normalize_array,
)


def dataframe_to_list(data: pd.DataFrame) -> Union[List[Dict], List]:
    """Converts DataFrame to a list of dictionaries"""
    if data.empty:
        return []
    return data.to_dict(orient='records')


def merge_dataframes(
        dataframes: List[pd.DataFrame],
        how: str,
        on: List[Union[int, float, str]],
    ) -> pd.DataFrame:
    """
    Merges list of DataFrames given.
    Parameters:
        - dataframes (list): List of DataFrames to merge.
        - how (str): The type of merge. Options: ['left', 'right', 'outer', 'inner', 'cross']
        - on (list): List of columns to merge on.
    """
    df_merged = reduce(
        lambda df_left, df_right: pd.merge(
            left=df_left,
            right=df_right,
            how=how,
            on=on,
        ),
        dataframes,
    )
    return df_merged


def drop_columns_if_exists(
        data: pd.DataFrame,
        columns: List[Union[int, float, str]],
    ) -> pd.DataFrame:
    """Drops list of given columns if they exist in the given DataFrame"""
    df = data.copy(deep=True)
    columns_available = df.columns.tolist()
    columns_to_drop = list(
        set(columns_available).intersection(set(columns))
    )
    if columns_to_drop:
        df.drop(labels=columns_to_drop, axis=1, inplace=True)
    return df


def transform_datetime_columns(
        data: pd.DataFrame,
        func: Callable,
        subset: Optional[List[Union[int, float, str]]] = None,
        column_prefix: Optional[str] = '',
        column_suffix: Optional[str] = '',
    ) -> pd.DataFrame:
    """
    Takes in a DataFrame, and applies the given function to all 'datetime64' columns in the DataFrame.
    Parameters:
        - data (DataFrame): Pandas DataFrame
        - func (callable): Callable Python function
        - subset (list): Subset of 'datetime64' columns to apply the function to (optional)
        - column_prefix (str): Prefix to add to column name, if you want to create new columns (optional)
        - column_suffix (str): Suffix to add to column name, if you want to create new columns (optional)
    """
    df = data.copy(deep=True)
    if subset:
        for column in subset:
            new_column = f"{column_prefix}{column}{column_suffix}"
            df[new_column] = df[column].apply(func=func)
    else:
        columns_with_datetimes = data.select_dtypes(include=['datetime64']).columns.tolist()
        for column in columns_with_datetimes:
            new_column = f"{column_prefix}{column}{column_suffix}"
            df[new_column] = df[column].apply(func=func)
    return df


def prettify_datetime_columns(
        data: pd.DataFrame,
        include_time: bool,
        subset: Optional[List[Union[int, float, str]]] = None,
        column_prefix: Optional[str] = '',
        column_suffix: Optional[str] = '',
    ) -> pd.DataFrame:
    """
    Takes in Pandas DataFrame, and converts all 'datetime64' columns to a more human readable format.
    Parameters:
        - data (DataFrame): Pandas DataFrame
        - include_time (bool): Includes time element if set to True
        - subset (list): Subset of datetime columns to prettify (optional)
        - column_prefix (str): Prefix to add to column name, if you want to create new columns (optional)
        - column_suffix (str): Suffix to add to column name, if you want to create new columns (optional)
    """
    df = data.copy(deep=True)
    formatter = "%d %B, %Y %I:%M %p" if include_time else "%d %B, %Y"
    df = transform_datetime_columns(
        data=df,
        func=lambda dt_obj: dt_obj.strftime(formatter),
        subset=subset,
        column_prefix=column_prefix,
        column_suffix=column_suffix,
    )
    return df


def add_partitioning_column(
        data: pd.DataFrame,
        num_partitions: int,
        column_name: str,
    ) -> pd.DataFrame:
    """
    Partitions a DataFrame horizontally, based on number of partitions given.
    Returns DataFrame with an additional column containing the partition number.
    """
    df = data.copy(deep=True)
    indices_for_partitioning = get_indices_for_partitioning(
        length_of_iterable=len(df),
        num_partitions=num_partitions,
    )
    partition_number = 0
    df_partitioned = pd.DataFrame()
    for i in range(len(indices_for_partitioning) - 1):
        partition_number += 1
        idx_start, idx_end = indices_for_partitioning[i], indices_for_partitioning[i+1]
        df_by_partition = df.iloc[idx_start : idx_end].copy()
        df_by_partition[column_name] = partition_number
        df_partitioned = pd.concat(objs=[df_partitioned, df_by_partition], ignore_index=True, sort=False)
    return df_partitioned


def partition_dataframe(
        data: pd.DataFrame,
        num_partitions: int,
    ) -> List[pd.DataFrame]:
    """
    Partitions a DataFrame horizontally, based on number of partitions given.
    Returns list of partitioned DataFrames.
    """
    list_of_dataframes = []
    indices_for_partitioning = get_indices_for_partitioning(length_of_iterable=len(data),
                                                            num_partitions=num_partitions)
    for i in range(len(indices_for_partitioning) - 1):
        idx_start, idx_end = indices_for_partitioning[i], indices_for_partitioning[i+1]
        df_by_partition = data.iloc[idx_start : idx_end]
        list_of_dataframes.append(df_by_partition)
    return list_of_dataframes


def switch_column_casing(
        data: pd.DataFrame,
        casing_type: str,
    ) -> pd.DataFrame:
    """
    Switch casing of columns in DataFrame.
    Options for `casing_type`:
        * 'sc2lcc': snake-case to lower-camel-case (Eg: some_text --> someText)
        * 'sc2ucc': snake-case to upper-camel-case (Eg: some_text --> SomeText)
        * 'lcc2sc': lower-camel-case to snake-case (Eg: someText --> some_text)
        * 'lcc2ucc': lower-camel-case to upper-camel-case (Eg: someText --> SomeText)
        * 'ucc2lcc': upper-camel-case to lower-camel-case (Eg: SomeText --> someText)
        * 'ucc2sc': upper-camel-case to snake-case (Eg: SomeText --> some_text)
    
    Note: Expects all columns present in DataFrame to be of same casing.
    """
    df = data.copy(deep=True)
    mapper = {
        'lcc2sc': lcc2sc,
        'lcc2ucc': lcc2ucc,
        'sc2lcc': sc2lcc,
        'sc2ucc': sc2ucc,
        'ucc2lcc': ucc2lcc,
        'ucc2sc': ucc2sc,
    }
    columns = df.columns.tolist()
    df.columns = list(map(mapper[casing_type], columns))
    return df


def round_off_columns(
        data: pd.DataFrame,
        columns: List[str],
        round_by: int,
    ) -> pd.DataFrame:
    """
    Rounds off specified numerical (float) columns in DataFrame.
    >>> round_off_columns(data=data, columns=['column1', 'column3', 'column5'], round_by=2)
    """
    df = data.copy(deep=True)
    for column in columns:
        df[column] = df[column].apply(round, args=[int(round_by)])
    return df


def add_ranking_column(
        data: pd.DataFrame,
        rank_column_name: Union[int, float, str],
        rank_by: List[Union[int, float, str]],
        ascending: List[bool],
    ) -> pd.DataFrame:
    """
    Adds ranking column to given DataFrame, based on `rank_by` column/s

    Parameters:
        - data (DataFrame): Pandas DataFrame
        - rank_column_name (int | float | str): Name of the ranking column (the column which will contain the actual ranking)
        - rank_by (list): List of columns to rank by
        - ascending (list): List of booleans signifying the order of ranking (must correspond to the columns in `rank_by`)
    """
    if len(rank_by) != len(ascending):
        raise ValueError(
            "Expected `rank_by` and `ascending` to be of same length,"
            f" but got lengths {len(rank_by)} and {len(ascending)} respectively"
        )
    df_ranked = data.sort_values(by=rank_by, ascending=ascending, ignore_index=True)
    rankings = np.arange(start=1, stop=len(df_ranked) + 1, step=1)
    df_ranked[rank_column_name] = rankings
    column_order = [rank_column_name] + df_ranked.drop(labels=[rank_column_name], axis=1).columns.tolist()
    df_ranked = df_ranked.loc[:, column_order]
    return df_ranked


def normalize_numerical_columns(
        data: pd.DataFrame,
        columns: List[Union[int, float, str]],
    ) -> pd.DataFrame:
    """
    Takes in DataFrame and list of numerical columns to normalize.
    Normalizes the given columns between [0-100].
    Note: Does not work with NaN values.
    """
    df = data.copy(deep=True)
    for column in columns:
        values = df[column].tolist()
        df[column] = normalize_array(array=values)
        df[column] = df[column].mul(100).round(2)
    return df


def randomly_fill_categorical_nans(
        data: pd.DataFrame,
        subset: Optional[List[Union[int, float, str]]] = None,
    ) -> pd.DataFrame:
    """
    Fills missing values of categorical columns by selecting random value from said column.
    Parameters:
        - data (DataFrame): Pandas DataFrame
        - subset (list): Subset of categorical columns for which you want to randomly fill missing values (optional)
    """
    df = data.copy(deep=True)
    categorical_variables = df.select_dtypes(include='object').columns.tolist()
    if subset:
        categorical_variables = list(set(categorical_variables).intersection(set(subset)))
    null_indicator_string = f"NULL-{get_current_timestamp_as_integer()}-{random.randint(1000, 9999)}"
    for cv in categorical_variables:
        if df[cv].isnull().sum() > 0:
            df[cv].fillna(value=null_indicator_string, inplace=True)
            unique_choices = df[cv].unique().tolist()
            unique_choices.remove(null_indicator_string)
            df[cv] = df[cv].apply(
                lambda string: random.choice(unique_choices) if ((string == null_indicator_string) and unique_choices) else string
            )
    return df