from typing import Dict, List, Optional, Union

from django.db.models import QuerySet
import pandas as pd

from pyutils.data_analysis.transform import (
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