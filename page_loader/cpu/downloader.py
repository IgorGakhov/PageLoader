from typing import Final

from page_loader.cpu.file_system_guide import DEFAULT_DIR, \
    check_destination, get_file_path, save_data_to_file
from page_loader.cpu.connector import load_page_text
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
    check_destination(destination)
    file_path = get_file_path(url, destination)
    logger.info(START_DOWNLOAD.format(url, destination))

    text = load_page_text(url)
    logger.info(PAGE_RECEIVED.format(url))

    html = process_resources(text, url, destination)
    save_data_to_file(html, file_path)
    logger.info(FINISH_DOWNLOAD.format(file_path))

    return str(file_path)
