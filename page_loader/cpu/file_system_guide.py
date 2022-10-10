import os
from pathlib import Path
from typing import Final, Optional

from page_loader.cpu.name_converter import \
    get_base_name, parse_url
from page_loader.logger import \
    STORAGE_PATH_NOT_FOUND, DIRECTORY_CREATION_ERROR


DEFAULT_DIR: Final[str] = os.getcwd()


def get_file_path(url: str, destination: str, ext: Optional[str] = None) -> Path:  # noqa: E501
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
        file_path (Path): Full path to the downloaded file.
    '''
    base_name = get_base_name(url)
    if ext is None:
        native_ext = parse_url(url, invert=True).get('ext')
        ext = native_ext if native_ext else 'html'

    file_name = f'{base_name}.{ext}'
    file_path = Path(destination).joinpath(file_name)

    return file_path


def get_dir_path(url: str, destination: str) -> Path:
    '''
    Description:
    ---
        Generates the full path of the resources folder to save the resources.

    Parameters:
    ---
        - url (str): Page being downloaded.
        - destination (str): Output directory.

    Return:
    ---
        dir_path (Path): Full path to the downloaded resources folder.
    '''
    base_name = get_base_name(url)

    dir_name = f'{base_name}_files'
    dir_path = Path(destination).joinpath(dir_name)

    return dir_path


def check_destination(destination: str) -> None:
    '''Checks if the entered save path is valid.'''
    if not os.path.exists(destination):
        raise ValueError(STORAGE_PATH_NOT_FOUND.format(destination))


def check_resources_dir(dir_path: Path) -> None:
    '''Checks for the existence of a directory to save resources
    and creates it if necessary.'''
    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path)
        except OSError:
            raise OSError(DIRECTORY_CREATION_ERROR.format(dir_path))
