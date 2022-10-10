import traceback

from page_loader.cpu.file_system_guide import DEFAULT_DIR, \
    check_destination, check_resources_dir, get_file_path, get_dir_path
from page_loader.cpu.connector import get_response
from page_loader.cpu.html_parser import replace_resources
from page_loader.cpu.saver import save, save_resources
from page_loader.logger import logger, \
    START_DOWNLOAD, PAGE_RECEIVED, FINISH_DOWNLOAD


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

        page = get_response(url)
        logger.info(PAGE_RECEIVED.format(url))

        dir_path = get_dir_path(url, destination)
        html, resources = replace_resources(page.text, url, dir_path)

        if resources:
            check_resources_dir(dir_path)
            save_resources(resources, dir_path)

        save(html, file_path)

    except Exception as error:
        logger.error(traceback.format_exc(1))
        raise error

    logger.info(FINISH_DOWNLOAD.format(file_path, dir_path))

    return str(file_path)
