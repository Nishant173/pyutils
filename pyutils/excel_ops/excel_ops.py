from typing import (
    Any,
    ByteString,
    Dict,
    List,
    Optional,
    Union,
)
import io

from django.http import HttpResponse
import pandas as pd

from pyutils.general.data_io import get_basename_from_filepath

Column = Union[int, float, str] # Type-hint for columns in a Pandas DataFrame


def style_dataframe_by_cell(
        df_style_obj: Any,
        props: List[Dict[str, Union[pd.Series, List[Column], Dict[str, str], None]]],
    ) -> Any:
    """
    Takes in Pandas Styler object (of class `pandas.io.formats.style.Styler`), and a list of `props`.
    Returns Pandas Styler object after applying the styles based on the given conditions (via `props`).
    Reference: https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html

    >>> num_rows = 50
    >>> df = pd.DataFrame(data={
        'column1': [np.random.randint(-25, 25) for _ in range(num_rows)],
        'column2': [np.random.randint(0, 100) for _ in range(num_rows)],
        'column3': [np.random.randint(-40, 15) for _ in range(num_rows)],
        'column4': [np.random.randint(-5, 5) for _ in range(num_rows)],
    })
    >>> style_dataframe_by_cell(
        df_style_obj=df.style,
        props=[
            {
                'row_conditions': (df['column1'] >= 10) | (df['column1'] % 2 == 0),
                'column_subset': ['column1', 'column2'],
                'styling_kwargs': {
                    'background-color': 'green',
                    'color': 'purple',
                },
            },
            {
                'row_conditions': (df['column3'] < 0),
                'column_subset': None,
                'styling_kwargs': {
                    'background-color': 'blue',
                    'color': 'orange',
                },
            },
            {
                'row_conditions': None,
                'column_subset': ['column4'],
                'styling_kwargs': {
                    'background-color': 'grey',
                    'color': 'red',
                },
            },
        ],
    )

    In the `props`, each prop is a dictionary having 3 keys: ['row_conditions', 'column_subset', 'styling_kwargs'].
    The keys 'row_conditions' and 'column_subset' can have a value of None.
    The key 'styling_kwargs' can have a value of {}.
    The ordering of the `props` matter i.e; if 5 props are given, the 4th prop can over-write the 3rd prop.
    """
    df_styled = df_style_obj.__copy__()
    idx = pd.IndexSlice
    for prop in props:
        row_conditions = prop['row_conditions']
        column_subset = prop['column_subset']
        styling_kwargs = prop['styling_kwargs']

        subset = idx[idx[row_conditions], column_subset]
        if row_conditions is None and column_subset is None:
            subset = None
        elif row_conditions is None and column_subset is not None:
            subset = idx[idx[:], column_subset]
        elif row_conditions is not None and column_subset is None:
            subset = idx[idx[row_conditions], :]
        df_styled = df_styled.set_properties(
            subset=subset,
            axis=1,
            **styling_kwargs,
        )
    return df_styled


def style_dataframe_with_background_gradient(
        df_style_obj: Any,
        blue_white_red: Optional[List[Column]] = None,
        blues: Optional[List[Column]] = None,
        greens: Optional[List[Column]] = None,
        red_yellow_green: Optional[List[Column]] = None,
        summer: Optional[List[Column]] = None,
    ) -> Any:
    """
    Takes in Pandas Styler object (of class `pandas.io.formats.style.Styler`), and returns the same
    after applying background gradient styles based on the given column subsets.
    """
    df_styled = df_style_obj.__copy__()
    if blue_white_red:
        df_styled = df_styled.background_gradient(subset=blue_white_red, cmap='bwr')
    if blues:
        df_styled = df_styled.background_gradient(subset=blues, cmap='Blues')
    if greens:
        df_styled = df_styled.background_gradient(subset=greens, cmap='Greens')
    if red_yellow_green:
        df_styled = df_styled.background_gradient(subset=red_yellow_green, cmap='RdYlGn')
    if summer:
        df_styled = df_styled.background_gradient(subset=summer, cmap='summer')
    return df_styled


def save_styled_dataframes(
        destination_filepath: str,
        sheet_name_to_df_styled: Dict[str, Any],
    ) -> None:
    """
    Saves Pandas Styler object/s to an Excel file, which could have multiple sheets (one for each DataFrame).
    >>> save_styled_dataframes(
        destination_filepath="resulting_file.xlsx",
        sheet_name_to_df_styled={
            "sheet1": df_styled_1,
            "sheet2": df_styled_2,
        },
    )
    """
    with pd.ExcelWriter(destination_filepath) as excel_writer:
        for sheet_name, df_styled in sheet_name_to_df_styled.items():
            df_styled.to_excel(
                excel_writer=excel_writer,
                sheet_name=sheet_name,
                index=False,
                engine='xlsxwriter',
            )
    return None


def get_all_excel_sheets(filepath: str) -> Dict[str, pd.DataFrame]:
    """
    Takes `filepath` to an Excel file. Returns dictionary having keys = sheet names, and
    values = DataFrame corresponding to respective sheet name.
    """
    excel_file = pd.ExcelFile(filepath, engine='openpyxl')
    sheet_names = excel_file.sheet_names
    dict_obj = {}
    for sheet_name in sheet_names:
        df_by_sheet = pd.read_excel(filepath, engine='openpyxl', sheet_name=sheet_name)
        dict_obj[sheet_name] = df_by_sheet
    return dict_obj


def excel_file_to_bytes(filepath: str) -> ByteString:
    """Takes `filepath` to an Excel file, and returns ByteString of the same"""
    bio = io.BytesIO()
    writer = pd.ExcelWriter(bio, engine='openpyxl')
    dict_all_excel_sheets = get_all_excel_sheets(filepath=filepath)
    for sheet_name, df_obj in dict_all_excel_sheets.items():
        df_obj.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    bytes_obj = bio.getvalue()
    return bytes_obj


def excel_file_to_django_http_response(filepath: str) -> HttpResponse:
    """
    Takes `filepath` to an Excel file, and returns Django HTTP Response object of the same.
    """
    filename = get_basename_from_filepath(filepath=filepath)
    content = open(file=filepath, mode='rb')
    response = HttpResponse(
        content=content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['X-Sendfile'] = filename
    return response