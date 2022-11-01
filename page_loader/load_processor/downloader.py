import threading
from pathlib import Path
from typing import List, Dict, Final, Union

from page_loader.load_processor.file_system_guide import DEFAULT_DIR, \
    check_destination, get_file_path, get_dir_path, make_resources_dir
from page_loader.load_processor.data_loader import \
    load_page_text, load_page_content
from page_loader.load_processor.html_parser import process_resources
from page_loader.load_processor.saver import save_page, save_resource
from page_loader.progress import Progress
from page_loader.logger import logger


START_DOWNLOAD: Final[str] = 'Initiated download of page {} \
to local directory «{}» ...'
PAGE_RECEIVED: Final[str] = 'Response from page {} received.\n\
Page available for download!'
FINISH_DOWNLOAD: Final[str] = 'FINISHED! Loading is complete successfully!\n\
The downloaded page is located in the «{}» file.\n'
START_RESOURCES_SAVING: Final[str] = 'Started saving page local resources ...'
FINISH_RESOURCES_SAVING: Final[str] = 'Finished saving page local resources.'
START_SAVE_RESOURCE: Final[str] = 'Saving the resource {}\n\
along the path «{}» ...'
FINISH_SAVE_RESOURCE: Final[str] = '[+] Resource {} saved successfully!'


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
    dir_path = get_dir_path(url, destination)
    logger.info(START_DOWNLOAD.format(url, destination))

    text = load_page_text(url)
    logger.info(PAGE_RECEIVED.format(url))

    html, resources = process_resources(text, url, dir_path)
    if len(resources):
        make_resources_dir(dir_path)
        download_resource_pack(resources)

    save_page(html, file_path)
    logger.info(FINISH_DOWNLOAD.format(file_path))

    return str(file_path)


def download_resource_pack(local_resources: List[Dict]) -> None:
    '''Traverses a set of tags and downloads the contents
    of their links to local storage.'''
    logger.debug(START_RESOURCES_SAVING)

    progress = Progress(len(local_resources))
    threads = []
    for resource in local_resources:
        stream = threading.Thread(
            target=download_resource,
            args=(resource, progress)
        )
        threads.append(stream)
        stream.start()

    [thread.join() for thread in threads]

    progress.downloading_resources_finish()
    logger.debug(FINISH_RESOURCES_SAVING)


def download_resource(resource: Dict[str, Union[str, Path]],
                      progress: Progress) -> None:
    '''Downloads the contents of a tag link to local storage.'''
    logger.debug(START_SAVE_RESOURCE.format(resource['link'], resource['path']))

    content = load_page_content(resource['link'])
    save_resource(content, resource['path'])

    progress.downloading_resources_next()
    logger.info(FINISH_SAVE_RESOURCE.format(resource['link']))
