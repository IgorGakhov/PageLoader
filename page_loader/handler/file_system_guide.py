import os
from typing import Final, Optional

from page_loader.handler.name_converter import \
    create_file_name, create_dir_name
from page_loader.logger import \
    STORAGE_PATH_NOT_FOUND, DIRECTORY_CREATION_ERROR


DEFAULT_DIR: Final[str] = os.getcwd()


def get_file_path(url: str, destination: str, ext: Optional[str] = None) -> str:  # noqa: E501
    '''
    Description:
    ---
        Generates the full path of the file to save the page.

    Parameters:
    ---
        - url (str): Page being downloaded.
        - destination (str): Output directory.
        ---
        - ext (str): Saved file extension
        (by default - the original file extension, if not - '*.html').

    Return:
    ---
        file_path (str): Full path to the downloaded file.
    '''
    if not os.path.exists(destination):
        raise ValueError(STORAGE_PATH_NOT_FOUND.format(destination))

    file_name = create_file_name(url, ext)
    file_path = os.path.join(destination, file_name)

    return file_path


def get_dir_path(url: str, destination: str, ext: Optional[str] = None) -> str:
    '''
    Description:
    ---
        Generates the full path of the resources folder to save the resources.

    Parameters:
    ---
        - url (str): Page being downloaded.
        - destination (str): Output directory.
        ---
        - ext (str): Saved folder extension
        (by default - the original folder extension, if not - '*_files').

    Return:
    ---
        dir_path (str): Full path to the downloaded resources folder.
    '''
    dir_name = create_dir_name(url, ext)
    dir_path = os.path.join(destination, dir_name)

    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError:
            raise OSError(DIRECTORY_CREATION_ERROR.format(dir_path))

    return dir_path
