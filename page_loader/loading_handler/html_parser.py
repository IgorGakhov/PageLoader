import os
from urllib.parse import urlparse, urljoin
from typing import Final

import requests
from bs4 import BeautifulSoup

from page_loader.loading_handler.file_system_guide import \
    parse_url, get_dir_name, HTML_EXT


TAGS_LINK_ATTRIBUTES: Final[dict] = {
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
    page = requests.get(url)
    html, resources = search_resources(page.text, url)

    save_resources(resources, dir_path)

    return html


def search_resources(html: str, page_url: str) -> tuple[str, list[dict]]:
    '''Replaces resource links with their paths in the file system,
    returns the processed html and download links of these resources.'''
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


def save_resources(resources: list, dir_path: str) -> None:
    '''Iterates through the passed list of resources,
    saves them locally at the given location.'''
    for resource in resources:
        content = requests.get(resource['link']).content
        resource_path = os.path.join(dir_path, resource['name'])

        with open(resource_path, 'wb') as file:
            file.write(content)
