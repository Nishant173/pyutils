from typing import Any, List, Optional
import json
import ntpath
import os

import joblib
import pandas as pd


def get_line_count(filepath: str) -> int:
    """Returns count of number of lines in the given file"""
    num_lines = sum(1 for _ in open(file=filepath))
    return num_lines


def get_extension(filepath: str) -> str:
    return os.path.splitext(filepath)[-1][1:]


def get_basename_from_filepath(filepath: str) -> str:
    """Returns base-name of the file in the given `filepath` (along with the extension)"""
    head, tail = ntpath.split(p=filepath)
    return tail or ntpath.basename(head)


def filter_filepaths_by_extensions(
        filepaths: List[str],
        extensions: List[str],
    ) -> List[str]:
    extensions = list(
        map(lambda extension: extension.strip().lower(), extensions)
    )
    filepaths_needed = list(
        filter(lambda filepath: get_extension(filepath=filepath).strip().lower() in extensions, filepaths)
    )
    return filepaths_needed


def get_filepaths(
        src_dir: str,
        extensions: Optional[List[str]] = None,
    ) -> List[str]:
    """
    Gets list of all filepaths from source directory (in the immediate directory).
    Note: The `src_dir` can be an r-string.
    >>> get_filepaths(src_dir="SOME_SRC_DIR", extensions=['csv', 'xlsx'])
    """
    filenames = os.listdir(src_dir)
    filepaths = [os.path.join(src_dir, filename) for filename in filenames]
    if extensions is not None:
        filepaths = filter_filepaths_by_extensions(filepaths=filepaths, extensions=extensions)
    return filepaths


def get_filepaths_multi_level(
        src_dir: str,
        extensions: Optional[List[str]] = None,
    ) -> List[str]:
    """
    Gets list of all filepaths from source directory (including all sub-directories).
    Note: The `src_dir` can be an r-string.
    >>> get_filepaths_multi_level(src_dir="SOME_SRC_DIR", extensions=['csv', 'xlsx'])
    """
    filepaths = []
    for path, _, files in os.walk(src_dir):
        for filename in files:
            filepath = os.path.join(path, filename)
            filepaths.append(filepath)
    if extensions is not None:
        filepaths = filter_filepaths_by_extensions(filepaths=filepaths, extensions=extensions)
    return filepaths


def get_line_count_dataframe(
        src_dir: str,
        extensions: List[str],
    ) -> pd.DataFrame:
    """
    Gets line-count of all filepaths from source directory (including all sub-directories).
    Returns DataFrame having columns: ['Filepath', 'LineCount'].
    >>> get_line_count_dataframe(src_dir="SOME_SRC_DIR", extensions=['py', 'js', 'txt'])
    """
    filepaths = get_filepaths_multi_level(src_dir=src_dir, extensions=extensions)
    # Keys = filepaths, and values = line count in each file
    dict_line_counts = {
        filepath : get_line_count(filepath=filepath) for filepath in filepaths
    }
    df_line_counts = pd.DataFrame(data={
        'Filepath': dict_line_counts.keys(),
        'LineCount': dict_line_counts.values(),
    })
    return df_line_counts


def pickle_load(filepath: str) -> Any:
    """Loads data from pickle file, via joblib module"""
    python_obj = joblib.load(filename=filepath)
    return python_obj


def pickle_save(data_obj: Any, filepath: str) -> None:
    """Saves data as pickle file, via joblib module"""
    joblib.dump(value=data_obj, filename=filepath)
    return None


def save_object_as_json(obj: Any, filepath: str) -> None:
    """Saves Python object as JSON file"""
    with open(file=filepath, mode='w') as fp:
        json.dump(obj=obj, fp=fp, indent=4)
    return None


def read_to_dataframe(filepath: str) -> pd.DataFrame:
    """Reads DataFrame from filepaths having any of the following extensions: ['csv', 'xlsx']"""
    extension = get_extension(filepath=filepath).lower()
    if extension == 'csv':
        data = pd.read_csv(filepath)
    elif extension == 'xlsx':
        data = pd.read_excel(filepath)
    else:
        raise ValueError(f"Expected filepath's extension to be in ['csv', 'xlsx'], but got '{extension}'")
    return data


def save_dataframe(
        data: pd.DataFrame,
        filepath: str,
    ) -> None:
    """Saves DataFrame to one of the following file types: ['csv', 'xlsx', 'json']"""
    extension = get_extension(filepath=filepath).lower()
    if extension == 'csv':
        data.to_csv(filepath, index=False)
    elif extension == 'xlsx':
        data.to_excel(filepath, index=False)
    elif extension == 'json':
        data.to_json(filepath, orient='records', indent=4)
    else:
        raise ValueError(f"Expected filepath's extension to be in ['csv', 'xlsx', 'json'], but got '{extension}'")
    return None