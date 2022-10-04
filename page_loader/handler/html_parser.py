import os
from urllib.parse import urlparse, urljoin
from typing import Final, Tuple, List, Dict

from bs4 import BeautifulSoup

from page_loader.handler.name_converter import \
    create_dir_name, create_resource_name
from page_loader.logger import logger, \
    START_PARSING, FOUND_RESOURCE, FINISH_PARSING


TAGS_LINK_ATTRIBUTES: Final[Dict] = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def replace_resources(html: str, page_url: str) -> Tuple[str, List[Dict]]:
    '''Replaces resource links with their paths in the file system,
    returns the processed html and download links of these resources.'''
    logger.debug(START_PARSING)

    dir_name = create_dir_name(page_url)

    soup = BeautifulSoup(html, 'html.parser')

    resources = []
    for resource_tag in TAGS_LINK_ATTRIBUTES.keys():
        for tag in soup.find_all(resource_tag):
            link_attr = TAGS_LINK_ATTRIBUTES[tag.name]

            link = get_full_link(tag[link_attr], page_url)
            if is_local_link(link, page_url):

                logger.debug(FOUND_RESOURCE.format(link))

                resource_name = create_resource_name(link)
                tag[link_attr] = os.path.join(dir_name, resource_name)

                resource = {
                    'link': link,
                    'name': resource_name
                }
                resources.append(resource)

    html = soup.prettify()

    logger.debug(FINISH_PARSING)

    return html, resources


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
