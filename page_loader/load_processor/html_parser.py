import os
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Tuple, Final, Optional

import bs4

from page_loader.load_processor.name_converter import create_resource_name
from page_loader.logger import logger


START_PARSING: Final[str] = 'Started HTML page parsing and \
replacing local resource links ...'
FINISH_PARSING: Final[str] = 'Finished HTML page parsing and \
replacing local resource links.'
FOUND_RESOURCE: Final[str] = '[!] Found resource {}.'


TAGS_LINK_ATTRIBUTES: Final[Dict[str, str]] = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def process_resources(html: str,
                      page_url: str,
                      resources_path: Path) -> Tuple[str, List]:
    '''
    Description:
    ---
        Returns a parsed html with local resource references that it
        downloads and places in a special directory if it doesn't exist.

    Parameters:
    ---
        - html (str): Content of the page.
        - page_url (str): Page being downloaded.
        - resources_path (Path): Resources directory.

    Return:
    ---
        html (str): Processed page content.
        local_resources (list): List of local resources.
    '''
    logger.debug(START_PARSING)

    soup = bs4.BeautifulSoup(html, 'html.parser')
    target_tags = soup.find_all(TAGS_LINK_ATTRIBUTES.keys())

    local_resources = []
    for tag in target_tags:
        link_attr = get_link_attribute(tag)

        link: Optional[str] = tag.get(link_attr)
        if not link:
            break

        full_link = get_full_link(link, page_url)
        if is_local_link(full_link, page_url):
            resource_name = create_resource_name(full_link)
            tag[link_attr] = os.path.join(resources_path.name, resource_name)

            resource = {
                'link': full_link,
                'path': Path(resources_path).joinpath(resource_name)
            }
            local_resources.append(resource)

    html = soup.prettify()

    logger.debug(FINISH_PARSING)

    return html, local_resources


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
