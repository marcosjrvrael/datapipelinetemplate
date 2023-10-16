"""Files helper module."""
import os
import re
import pathlib
from typing import List


def get_dir_files(path: str) -> List[str]:
    """Load files or subdirs inside a dir.

    Args:
        path (str): files path.

    Returns:
        List[str]: a list containg all files in a path.
    """
    return os.listdir(path)


def file_name_without_extension(file_name: str) -> str:
    """Return the same dir_name without .json extension.

    Args:
        file_name (str): File name

    Returns:
        [str]: same file name withou extension
    """
    return re.sub(r"\.[^.]*$", "", file_name)


def create_dir_if_not_exist(path: str):
    """Create data folder structure if not exits."""
    # os.makedirs(path, exist_ok=True)
    pathdir = pathlib.Path(path)
    pathdir.mkdir(parents=True, exist_ok=True)

