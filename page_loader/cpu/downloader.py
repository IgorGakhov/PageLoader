from typing import Final

import traceback

from page_loader.cpu.file_system_guide import DEFAULT_DIR, \
    check_destination, get_file_path, save_data_to_file
from page_loader.cpu.connector import get_response_content
from page_loader.cpu.html_parser import process_resources
from page_loader.logger import logger


START_DOWNLOAD: Final[str] = 'Initiated download of page {} \
to local directory «{}» ...'
PAGE_RECEIVED: Final[str] = 'Response from page {} received.\n\
Page available for download!'
FINISH_DOWNLOAD: Final[str] = 'FINISHED! Loading is complete successfully!\n\
The downloaded page is located in the «{}» file.\n'


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
    try:
        check_destination(destination)
        file_path = get_file_path(url, destination)
        logger.info(START_DOWNLOAD.format(url, destination))

        content = get_response_content(url)
        logger.info(PAGE_RECEIVED.format(url))

        html = process_resources(content, url, destination)
        save_data_to_file(html, file_path)

    except Exception as error:
        logger.error(traceback.format_exc(1))
        raise error

    logger.info(FINISH_DOWNLOAD.format(file_path))

    return str(file_path)
