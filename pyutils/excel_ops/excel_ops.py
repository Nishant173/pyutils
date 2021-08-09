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

Column = Union[int, float, str] # Type-hint for columns in a Pandas DataFrame


def style_dataframe(
        data: pd.DataFrame,
        blue_white_red: Optional[List[Column]] = None,
        blues: Optional[List[Column]] = None,
        greens: Optional[List[Column]] = None,
        red_yellow_green: Optional[List[Column]] = None,
        summer: Optional[List[Column]] = None,
    ) -> Any:
    """Styles DataFrame and returns Styler object (of class `pandas.io.formats.style.Styler`)"""
    df = data.copy(deep=True)
    df_style_obj = df.style
    if blue_white_red:
        df_style_obj = df_style_obj.background_gradient(subset=blue_white_red, cmap='bwr')
    if blues:
        df_style_obj = df_style_obj.background_gradient(subset=blues, cmap='Blues')
    if greens:
        df_style_obj = df_style_obj.background_gradient(subset=greens, cmap='Greens')
    if red_yellow_green:
        df_style_obj = df_style_obj.background_gradient(subset=red_yellow_green, cmap='RdYlGn')
    if summer:
        df_style_obj = df_style_obj.background_gradient(subset=summer, cmap='summer')
    return df_style_obj


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