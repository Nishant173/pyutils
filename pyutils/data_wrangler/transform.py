from typing import Any, Callable, Dict, List, Optional, Union
from collections import Counter
from functools import reduce
import random

import numpy as np
import pandas as pd

from pyutils.core.date_ops import get_current_timestamp_as_integer
from pyutils.core.text_casing import (
    lcc2sc,
    lcc2ucc,
    sc2lcc,
    sc2ucc,
    ucc2lcc,
    ucc2sc,
)
from pyutils.core.type_annotations import (
    Number,
    NumberOrString,
)
from pyutils.core.utils import get_indices_for_partitioning


def spread_array_by_factor(
        array: List[Number],
        factor: int,
    ) -> List[Number]:
    """
    Spread out an array by given factor.
    >>> spread_array_by_factor(array=[4, 6, 7, 3], factor=3)
    >>> [4, 4, 4, 6, 6, 6, 7, 7, 7, 3, 3, 3]
    """
    array_after_spreading = []
    for idx, _ in enumerate(array):
        array_after_spreading += [array[idx]] * int(factor)
    return array_after_spreading


def spread_array_by_length(
        array: List[Number],
        to: int,
    ) -> List[Number]:
    """
    Definition:
        Spread out an array to particular length without distorting signal of the original data.
    Parameters:
        - array (list): List or list-like array data
        - to (int): Length of array to be spread into
    >>> spread_array_by_length(array=[2, 3, -7], to=14)
    >>> [2, 2, 2, 2, 3, 3, 3, 3, 3, -7, -7, -7, -7, -7]
    """
    initial_array_length = len(array)
    if initial_array_length >= to:
        return array
    array_after_spread = []
    spread_factor = to / initial_array_length
    # If length of array to spread into is divisible by length of initial array
    if int(spread_factor) == spread_factor:
        array_after_spread = spread_array_by_factor(array=array, factor=int(spread_factor))
        return array_after_spread
    # Perform necessary complete fill-ups of the array to spread into
    num_complete_fillups = int(np.floor(spread_factor))
    if num_complete_fillups > 0:
        array_after_spread = spread_array_by_factor(array=array, factor=num_complete_fillups)
    # Fill-up the remaining elements of `array_after_spread` randomly (to minimise distortion)
    while len(array_after_spread) != to:
        random_index = random.randint(0, len(array_after_spread)-1)
        random_element = array_after_spread[random_index]
        array_after_spread.insert(random_index+1, random_element)
    return array_after_spread


def linspace_by_index(
        array: List[Any],
        how_many: int,
    ) -> List[Any]:
    """
    Gets linspaced values from array (based on indices of the array).
    >>> array = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96]
    >>> linspace_by_index(array=array, how_many=4) # Returns [0, 32, 64, 96]
    >>> linspace_by_index(array=array, how_many=5) # Returns [0, 24, 48, 72, 96]
    """
    linspaced_indices = list(np.linspace(start=0, stop=len(array) - 1, num=how_many))
    linspaced_indices = list(map(np.ceil, linspaced_indices))
    linspaced_indices = list(map(int, linspaced_indices))
    linspaced_values = [array[idx] for idx in linspaced_indices]
    return linspaced_values


def normalize_array(array: List[Number]) -> List[Number]:
    """
    Normalizes values in array to range of [0, 1].
    Ignores and removes all NaNs.
    """
    array = np.array(array)
    array = array[~np.isnan(array)]
    normalized_array = (array - np.min(array)) / np.ptp(array)
    return list(normalized_array)


def dataframe_to_list(data: pd.DataFrame) -> Union[List[Dict], List]:
    """Converts DataFrame to a list of dictionaries"""
    if data.empty:
        return []
    return data.to_dict(orient='records')


def stringify_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Converts all column names of the given DataFrame to strings (in case some of them are int/float)"""
    df = data.copy(deep=True)
    df.columns = list(map(str, df.columns.tolist()))
    return df


def merge_dataframes(
        dataframes: List[pd.DataFrame],
        how: str,
        on: List[NumberOrString],
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
        columns: List[NumberOrString],
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
        subset: Optional[List[NumberOrString]] = None,
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
        subset: Optional[List[NumberOrString]] = None,
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
    indices_for_partitioning = get_indices_for_partitioning(
        length_of_iterable=len(data),
        num_partitions=num_partitions,
    )
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
        columns: List[NumberOrString],
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


def __get_row_number_rankings(df_ranked: pd.DataFrame) -> List[int]:
    row_number_rankings = list(
        np.arange(start=1, stop=len(df_ranked) + 1, step=1)
    )
    return row_number_rankings


def __get_dense_rankings(
        df_ranked: pd.DataFrame,
        rank_by: List[NumberOrString],
    ) -> List[int]:
    dense_rankings = [1]
    values_used_for_ranking = list(df_ranked[rank_by].itertuples(index=False))
    prev = values_used_for_ranking[0]
    for value in values_used_for_ranking[1:]:
        latest_rank_assigned = dense_rankings[-1]
        ranking_for_row = latest_rank_assigned if prev == value else latest_rank_assigned + 1
        dense_rankings.append(ranking_for_row)
        prev = value
    return dense_rankings


def __get_non_dense_rankings(
        df_ranked: pd.DataFrame,
        rank_by: List[NumberOrString],
    ) -> List[int]:
    non_dense_rankings = [1]
    values_used_for_ranking = list(df_ranked[rank_by].itertuples(index=False))
    prev = values_used_for_ranking[0]
    for value in values_used_for_ranking[1:]:
        latest_rank_assigned = non_dense_rankings[-1]
        ranking_for_row = latest_rank_assigned if prev == value else latest_rank_assigned + Counter(non_dense_rankings)[latest_rank_assigned]
        non_dense_rankings.append(ranking_for_row)
        prev = value
    return non_dense_rankings


def rank_and_sort(
        data: pd.DataFrame,
        rank_column_name: NumberOrString,
        rank_by: List[NumberOrString],
        ascending: List[bool],
        method: str,
    ) -> pd.DataFrame:
    """
    Adds ranking column and sorts records based on the `rank_by` column/s.

    Parameters:
        - data (DataFrame): Pandas DataFrame.
        - rank_column_name (int | float | str): Name of the ranking column (the column which will contain the actual ranking).
        - rank_by (list): List of columns to rank by.
        - ascending (list): List of booleans signifying the order of ranking (must correspond to the columns in `rank_by`).
        - method (str): Type of ranking to be used. Options: ['row_number', 'dense_rank', 'non_dense_rank'].
    
    |    | column   |   row_number |   dense_rank |   non_dense_rank |
    |---:|:---------|-------------:|-------------:|-----------------:|
    |  0 | a        |            1 |            1 |                1 |
    |  1 | a        |            2 |            1 |                1 |
    |  2 | a        |            3 |            1 |                1 |
    |  3 | a        |            4 |            1 |                1 |
    |  4 | b        |            5 |            2 |                5 |
    |  5 | b        |            6 |            2 |                5 |
    |  6 | c        |            7 |            3 |                7 |
    |  7 | d        |            8 |            4 |                8 |
    |  8 | d        |            9 |            4 |                8 |
    |  9 | e        |           10 |            5 |               10 |
    | 10 | e        |           11 |            5 |               10 |
    | 11 | f        |           12 |            6 |               12 |
    | 12 | g        |           13 |            7 |               13 |
    | 13 | g        |           14 |            7 |               13 |
    """
    method_options = ['row_number', 'dense_rank', 'non_dense_rank']
    if method not in method_options:
        raise ValueError(f"Expected `method` to be in {method_options}, but got '{method}'")
    if len(rank_by) != len(ascending):
        raise ValueError(
            "Expected `rank_by` and `ascending` to be of same length,"
            f" but got lengths {len(rank_by)} and {len(ascending)} respectively."
        )
    df_ranked = data.sort_values(by=rank_by, ascending=ascending, ignore_index=True).copy(deep=True)
    if method == 'row_number':
        rankings = __get_row_number_rankings(df_ranked=df_ranked)
    elif method == 'dense_rank':
        rankings = __get_dense_rankings(df_ranked=df_ranked, rank_by=rank_by)
    elif method == 'non_dense_rank':
        rankings = __get_non_dense_rankings(df_ranked=df_ranked, rank_by=rank_by)
    df_ranked[rank_column_name] = rankings
    column_order = [rank_column_name] + df_ranked.drop(labels=[rank_column_name], axis=1).columns.tolist()
    df_ranked = df_ranked.loc[:, column_order]
    return df_ranked


def normalize_numerical_columns(
        data: pd.DataFrame,
        columns: List[NumberOrString],
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
        subset: Optional[List[NumberOrString]] = None,
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