import os
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Final, Optional, Union

import bs4

from page_loader.load_processor.file_system_guide import initialize_resources_dir  # noqa: E501
from page_loader.load_processor.name_converter import create_resource_name
from page_loader.load_processor.data_loader import load_page_content
from page_loader.load_processor.saver import save_resource
from page_loader.progress import Progress
from page_loader.logger import logger


START_PARSING: Final[str] = 'Started HTML page parsing and \
replacing local resource links ...'
FINISH_PARSING: Final[str] = 'Finished HTML page parsing and \
replacing local resource links.'
FOUND_RESOURCE: Final[str] = '[!] Found resource {}.'
START_RESOURCES_SAVING: Final[str] = 'Started saving page local resources ...'
FINISH_RESOURCES_SAVING: Final[str] = 'Finished saving page local resources.'
START_SAVE_RESOURCE: Final[str] = 'Saving the resource {}\n\
along the path «{}» ...'
FINISH_SAVE_RESOURCE: Final[str] = '[+] Resource {} saved successfully!'


TAGS_LINK_ATTRIBUTES: Final[Dict[str, str]] = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def process_resources(html: str, page_url: str, destination: str) -> str:
    '''
    Description:
    ---
        Returns a parsed html with local resource references that it
        downloads and places in a special directory if it doesn't exist.

    Parameters:
    ---
        - html (str): Content of the page.
        - url (str): Page being downloaded.
        - destination (str): Output directory.

    Return:
    ---
        html (str): Processed page content.
    '''
    logger.debug(START_PARSING)

    soup = bs4.BeautifulSoup(html, 'html.parser')
    target_tags = soup.find_all(TAGS_LINK_ATTRIBUTES.keys())

    if len(target_tags):
        dir_path = initialize_resources_dir(page_url, destination)

        local_resources = []
        for tag in target_tags:
            link_attr = get_link_attribute(tag)

            link: Optional[str] = tag.get(link_attr)
            if not link:
                break

            full_link = get_full_link(link, page_url)
            if is_local_link(full_link, page_url):
                resource_name = create_resource_name(full_link)
                tag[link_attr] = os.path.join(dir_path.name, resource_name)

                resource = {
                    'link': full_link,
                    'path': Path(dir_path).joinpath(resource_name)
                }
                local_resources.append(resource)

        download_resource_pack(local_resources)

    html = soup.prettify()

    logger.debug(FINISH_PARSING)

    return html


def download_resource_pack(local_resources: List[Dict]) -> None:
    '''Traverses a set of tags and downloads the contents
    of their links to local storage.'''
    logger.debug(START_RESOURCES_SAVING)

    progress = Progress(len(local_resources))
    for resource in local_resources:
        # ToDo: implement multi-threaded loading ...
        download_resource(resource, progress)

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


def get_link_attribute(tag: bs4.element.Tag) -> str:
    '''Returns the relevant source attribute for the selected tag,
    for example 'img' -> 'src'.'''
    return TAGS_LINK_ATTRIBUTES[tag.name]


def get_full_link(link: str, page_url: str) -> str:
    '''Returns the full URL of the link.'''
    scheme = urlparse(page_url).scheme
    netloc = urlparse(page_url).netloc
    url_domain_address = f'{scheme}://{netloc}'

    rsc_netloc = urlparse(link).netloc
    if not rsc_netloc:
        link = urljoin(url_domain_address, link)

    return link


def is_local_link(link: str, page_url: str) -> bool:
    '''Checks if the resource is local to the downloaded page.'''
    rsc_netloc = urlparse(link).netloc
    url_netloc = urlparse(page_url).netloc

    return rsc_netloc == url_netloc
