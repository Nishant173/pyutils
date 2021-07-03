from typing import Any, Dict, List, Optional, Union

import pandas as pd

Column = Union[int, float, str]


def style_dataframe(
        data: pd.DataFrame,
        greens: Optional[List[Column]] = None,
        blues: Optional[List[Column]] = None,
    ) -> Any:
    """Styles DataFrame and returns Styler object"""
    if not greens and not blues:
        raise ValueError(
            "Expects `greens` and/or `blues` in order to style said columns"
        )
    df = data.copy(deep=True)
    # Color mapping options: ['bwr', 'Greens', 'Blues', 'RdYlGn', 'summer']
    df = df.style\
        .background_gradient(subset=greens, cmap='Greens')\
        .background_gradient(subset=blues, cmap='Blues')
    return df


def save_styled_dataframe(
        filepath_with_ext: str,
        sheet_name_to_styler: Dict[str, Any],
    ) -> None:
    """Saves Pandas Styler object/s to an Excel file, which could have multiple sheets"""
    with pd.ExcelWriter(filepath_with_ext) as excel_writer:
        for sheet_name, styler_obj in sheet_name_to_styler.items():
            styler_obj.to_excel(
                excel_writer=excel_writer,
                sheet_name=sheet_name,
                index=False,
                engine='xlsxwriter',
            )
    return None