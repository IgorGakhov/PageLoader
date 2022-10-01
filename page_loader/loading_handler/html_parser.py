import os
import threading
from urllib.parse import urlparse, urljoin
from typing import Final, Tuple, List, Dict

import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.loading_handler.file_system_guide import \
    parse_url, get_dir_name, HTML_EXT
from page_loader.logger import logger, \
    START_PARSING, FINISH_PARSING, START_SEARCHING, FINISH_SEARCHING, \
    START_SAVING, FINISH_SAVING, START_GET_RESOURCE, FINISH_GET_RESOURCE, \
    START_SAVE_RESOURCE, FINISH_SAVE_RESOURCE, START_REQUEST, FINISH_REQUEST, \
    REQUEST_ERROR


TAGS_LINK_ATTRIBUTES: Final[Dict] = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}
DOMAIN_ADDRESS: Final[str] = '{}://{}'


def parse_page(url: str, dir_path: str) -> str:
    '''
    Description:
    ---
        Gets the content of a web page, processes links,
        downloads local resources, and returns the rendered HTML.

    Parameters:
    ---
        - url (str): Page being downloaded.
        - dir_path (str): Full path of the directory in the file system.

    Return:
    ---
        html (str): Processed HTML page with replaced links.
    '''
    logger.debug(START_PARSING)

    page = get_response(url)

    html, resources = search_resources(page.text, url)
    save_resources(resources, dir_path)

    logger.debug(FINISH_PARSING)

    return html


def get_response(url: str) -> requests.Response:
    '''Gets the response to a page request.'''
    logger.debug(START_REQUEST.format(url))

    try:
        page = requests.get(url)
        if page.status_code == requests.codes.ok:
            logger.info(FINISH_REQUEST.format(url))
            return page
        else:
            raise requests.exceptions.ConnectionError

    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(REQUEST_ERROR.format(url))


def search_resources(html: str, page_url: str) -> Tuple[str, List[Dict]]:
    '''Replaces resource links with their paths in the file system,
    returns the processed html and download links of these resources.'''
    logger.debug(START_SEARCHING)

    dir_name = get_dir_name(page_url)

    soup = BeautifulSoup(html, 'html.parser')

    resources = []
    for resource_tag in TAGS_LINK_ATTRIBUTES.keys():
        for tag in soup.find_all(resource_tag):
            link_attr = TAGS_LINK_ATTRIBUTES[tag.name]

            link = get_full_link(tag[link_attr], page_url)
            if is_local_link(link, page_url):

                resource_name = create_resource_name(link)
                tag[link_attr] = os.path.join(dir_name, resource_name)

                resource = {
                    'link': link,
                    'name': resource_name
                }
                resources.append(resource)

    html = soup.prettify()

    logger.debug(FINISH_SEARCHING)

    return html, resources


def get_full_link(link: str, page_url: str) -> str:
    '''Returns the full URL of the link.'''
    url_domain_address = DOMAIN_ADDRESS.format(
        urlparse(page_url).scheme, urlparse(page_url).netloc
    )

    rsc_netloc = urlparse(link).netloc
    if not rsc_netloc:
        link = urljoin(url_domain_address, link)

    return link


def is_local_link(link: str, page_url: str) -> bool:
    '''Checks if the resource is local to the downloaded page.'''
    rsc_netloc = urlparse(link).netloc
    url_netloc = urlparse(page_url).netloc

    return rsc_netloc == url_netloc


def create_resource_name(link: str) -> str:
    '''Formats a resource link and returns a name for the storage file
    (without the name of the storage directory).'''
    parsed_resource_link = parse_url(link)
    netloc = parsed_resource_link['netloc']
    path = parsed_resource_link['path']
    ext = parsed_resource_link['ext']
    ext = ext if ext else HTML_EXT

    resource_name = f'{netloc}-{path}.{ext}'

    return resource_name


def save_resources(resources: List, dir_path: str) -> None:
    '''Iterates through the passed list of resources,
    saves them locally at the given location.'''
    logger.debug(START_SAVING)

    bar = IncrementalBar(
        'Resources Loading',
        max=len(resources),
        suffix='%(percent)d%%   [' + IncrementalBar.suffix + ']\n'
    )

    threads = []
    for resource in resources:

        stream = threading.Thread(
            target=resource_save_thread,
            args=(resource, dir_path, bar)
        )
        threads.append(stream)
        stream.start()

    [thread.join() for thread in threads]

    bar.finish()

    logger.debug(FINISH_SAVING)


def resource_save_thread(resource: Dict, dir_path: str, bar: IncrementalBar) -> None:  # noqa: E501
    '''Stores a resource locally.'''
    logger.debug(START_GET_RESOURCE.format(resource['link']))

    content = requests.get(resource['link']).content

    logger.debug(FINISH_GET_RESOURCE.format(resource['link']))

    resource_path = os.path.join(dir_path, resource['name'])

    logger.debug(
        START_SAVE_RESOURCE.format(resource['link'], resource_path)
    )

    with open(resource_path, 'wb') as file:
        file.write(content)

    logger.info(FINISH_SAVE_RESOURCE.format(resource['link']))

    return bar.next()