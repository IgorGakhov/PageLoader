import os
from typing import Final

from page_loader.loading_handler.file_system_guide import get_file_path, get_dir_path  # noqa: E501
from page_loader.loading_handler.html_parser import parse_page
from page_loader.logger import logger, \
    START_DOWNLOAD, END_DOWNLOAD


DEFAULT_DIR: Final[str] = os.getcwd()


def download(url: str, destination: str = DEFAULT_DIR) -> str:
    '''
    Description:
    ---
        Downloads a page from the network
        and puts it in the specified existing directory.

    Parameters:
    ---
        - url (str): Page being downloaded.
        ---
        - destination (str): Output directory
        (by default, to the program launch directory).

    Return:
    ---
        file_path (str): Full path to the downloaded file.
    '''
    logger.info(START_DOWNLOAD.format(url, destination))

    file_path = get_file_path(url, destination)
    dir_path = get_dir_path(url, destination)

    html = parse_page(url, dir_path)

    with open(file_path, 'w') as file:
        file.write(html)

    logger.info(END_DOWNLOAD.format(file_path, dir_path))

    return file_path
