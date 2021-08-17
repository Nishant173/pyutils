from typing import Dict, List, Optional, Union
import mimetypes

from django.db.models import QuerySet
from django.http import HttpResponse
import pandas as pd

from pyutils.core.file_io import get_basename_from_filepath
from pyutils.data_wrangler.transform import (
    dataframe_to_list,
    drop_columns_if_exists,
)


def queryset_to_dataframe(
        qs: QuerySet,
        fields_to_drop: Optional[List[str]] = None,
    ) -> pd.DataFrame:
    df = pd.DataFrame(data=list(qs.values()))
    if fields_to_drop:
        df = drop_columns_if_exists(data=df, columns=fields_to_drop)
    return df


def queryset_to_list(
        qs: QuerySet,
        fields_to_drop: Optional[List[str]] = None,
    ) -> Union[List[Dict], List]:
    df = queryset_to_dataframe(qs=qs, fields_to_drop=fields_to_drop)
    list_of_dicts = dataframe_to_list(data=df)
    return list_of_dicts


def file_to_django_http_response(filepath: str) -> HttpResponse:
    """
    Converts the given file to Django HTTP Response object.
    Works for the following file extensions: ['csv', 'docx', 'flv', 'jpg', 'm4a', 'mp3', 'mp4', 'pdf', 'png', 'txt', 'xls', 'xlsx', 'zip'].
    """
    type_, encoding = mimetypes.guess_type(url=filepath)
    filename = get_basename_from_filepath(filepath=filepath)
    if type_ is None or encoding is not None:
        type_ = 'application/octet-stream'
    with open(file=filepath, mode='rb') as fp:
        http_response = HttpResponse(content=fp, content_type=type_)
    http_response['Content-Disposition'] = f'attachment; filename="{filename}"'
    http_response['X-Sendfile'] = filename
    return http_response