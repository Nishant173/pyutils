from typing import Any, List
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


def get_filepaths(
        src_dir: str,
        extensions: List[str],
    ) -> List[str]:
    """
    Gets list of all filepaths having particular extension/s from source directory.
    Note: The `src_dir` can be an r-string.
    >>> get_filepaths(src_dir="SOME_SRC_DIR", extensions=['csv', 'xlsx'])
    """
    extensions = [str(extension).strip().lower() for extension in extensions]
    filenames = os.listdir(src_dir)
    filenames = [filename for filename in filenames if get_extension(filename).lower() in extensions]
    filepaths = [os.path.join(src_dir, filename) for filename in filenames]
    return filepaths


def get_filepaths_multi_level(
        src_dir: str,
        extensions: List[str],
    ) -> List[str]:
    """
    Gets list of all filepaths having particular extension/s from all files in all
    sub-directories (if any) in the given source directory.
    Note: The `src_dir` can be an r-string.
    >>> get_filepaths_multi_level(src_dir="SOME_SRC_DIR", extensions=['csv', 'xlsx'])
    """
    extensions = list(map(lambda extension: extension.strip().lower(), extensions))
    filepaths = []
    for path, _, files in os.walk(src_dir):
        for filename in files:
            filepath = os.path.join(path, filename)
            extension = get_extension(filepath=filepath)
            extension = extension.strip().lower()
            if extension in extensions:
                filepaths.append(filepath)
    return filepaths


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