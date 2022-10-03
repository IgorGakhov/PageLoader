import traceback

from page_loader.loading_handler.file_system_guide import get_file_path, \
    DEFAULT_DIR
from page_loader.loading_handler.html_parser import parse_page
from page_loader.logger import logger, \
    START_DOWNLOAD, FINISH_DOWNLOAD


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
        file_path = get_file_path(url, destination)

        logger.info(START_DOWNLOAD.format(url, destination))

        html = parse_page(url, destination)

        with open(file_path, 'w') as file:
            file.write(html)

    except Exception as error:
        logger.error(traceback.format_exc(1))
        raise error

    logger.info(FINISH_DOWNLOAD.format(file_path))

    return file_path
