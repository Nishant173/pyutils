from typing import Dict, List, Union

import numpy as np
import pandas as pd

from pyutils.core.string_ops import remove_last_n_characters


def wrap_string_with_appropriate_quotes(text: str):
    """
    If given string contains single quotes, then wraps it with double quotes.
    If given string contains double quotes, then wraps it with single quotes.
    """
    if "'" in text:
        return f'"{text}"'
    return f"'{text}'"


def get_in_query_for_numbers(numbers: List[Union[int, float]]) -> str:
    comma_separated_numbers = ", ".join(map(str, numbers))
    return f"({comma_separated_numbers})"


def get_in_query_for_strings(strings: List[str]) -> str:
    comma_separated_strings = ", ".join(map(lambda string: wrap_string_with_appropriate_quotes(text=string), strings))
    return f"({comma_separated_strings})"


def __wrap_value_by_sql_datatype(
        value: Union[int, float, str, None],
        datatype: str,
    ) -> Union[int, float, str]:
    # Handle nulls
    if value is None:
        return 'null'
    if datatype in ['integer', 'float']:
        if np.isnan(value):
            return 'null'
    
    # Handle non-nulls
    if datatype == 'integer':
        return int(value)
    elif datatype == 'float':
        return float(value)
    elif datatype == 'string':
        if isinstance(value, str):
            return wrap_string_with_appropriate_quotes(text=value)
        return f"'{value}'"
    elif datatype == 'date':
        return f"DATE('{value}')"
    elif datatype == 'timestamp':
        return f"TIMESTAMP('{value}')"
    raise ValueError(f"Got unexpected option for `datatype`: '{datatype}'")


def __get_query_string_of_records(
        records: List[Dict],
        columns: List[str],
        datatypes: List[str],
    ) -> str:
    query = ""
    for record in records:
        values_per_record = []
        for column, datatype in zip(columns, datatypes):
            value = __wrap_value_by_sql_datatype(
                value=record[column],
                datatype=datatype,
            )
            values_per_record.append(value)
        comma_separated_values = ', '.join(map(str, values_per_record))
        query += f"({comma_separated_values}),\n"
    query = remove_last_n_characters(text=query, num_chars=2)
    return query


def generate_insert_query(
        data: pd.DataFrame,
        table_name: str,
        column_to_datatype_mapper: Dict[str, str],
    ) -> str:
    """
    Takes in DataFrame having the data to be inserted into a table.
    Returns an INSERT query (string) for the given DataFrame.
    Evaluates Python's None and Numpy's NaN to be null values.

    Accepted data-type options for the columns in the DataFrame:
        - integer
        - float
        - string
        - date: Values must be strings of format "yyyy-mm-dd". Eg: "2020-03-15"
        - timestamp: Values must be strings of format: "yyyy-mm-dd hh:mm:ss". Eg: "2020-03-15 19:30:55"
    
    >>> generate_insert_query(
            data=data, # Any DataFrame
            table_name='employee',
            column_to_datatype_mapper={
                'name': 'string',
                'age': 'integer',
                'date_of_birth': 'date',
                'joined_at': 'timestamp',
                'salary': 'float',
            },
        )
    """
    records = data.to_dict(orient='records')
    columns = data.columns.tolist()
    datatypes = list(map(lambda column: column_to_datatype_mapper[column], columns))
    comma_separated_columns = ', '.join(map(str, columns))
    query = f"INSERT INTO `{table_name}` ({comma_separated_columns})"
    query += "\nVALUES\n"
    query += __get_query_string_of_records(records=records, columns=columns, datatypes=datatypes)
    return query