from typing import ByteString, Dict
import io

from django.http import HttpResponse
import pandas as pd


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


def excel_file_to_http_response(
        source_filepath: str,
        destination_filename: str,
    ) -> HttpResponse:
    """
    Takes filepath to an Excel file, and returns Django HTTP Response object containing said Excel file.
    
    Parameters:
        - source_filepath (str): Filepath to the source Excel file (along with extension).
        - destination_filename (str): Filename of the destination Excel file (along with extension).
    
    Note: Does not work with formatted Excel files i.e; files with coloring, charts, etc.
    """
    bytes_obj = excel_file_to_bytes(filepath=source_filepath)
    response = HttpResponse(
        content=bytes_obj,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response['Content-Disposition'] = f'attachment; filename="{destination_filename}"'
    response['X-Sendfile'] = destination_filename
    return response