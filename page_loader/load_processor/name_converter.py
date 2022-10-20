import os
import re
from urllib.parse import urlparse
from typing import Dict, Final


USER_PASSWORD: Final[re.Pattern] = re.compile(r'.*@')  # for Network location
NOT_WORD: Final[re.Pattern] = re.compile(r'\W')
HYPHENS_AROUND: Final[re.Pattern] = re.compile(r'(^-*)|(-*$)')


def create_resource_name(link: str) -> str:
    '''Formats a resource link and returns a name for the storage file
    (without the name of the storage directory).'''
    parsed_resource_link = parse_url(link, invert=True)
    netloc = parsed_resource_link['netloc']
    path = parsed_resource_link['path']
    ext = parsed_resource_link['ext']
    ext = ext if ext else 'html'

    resource_name = f'{netloc}-{path}.{ext}'

    return resource_name


def get_base_name(url: str) -> str:
    '''Generates a base name for datastores.'''
    url_map = parse_url(url, invert=True)

    netloc = url_map['netloc']
    path = '-' + url_map['path'] if url_map['path'] else ''

    return netloc + path


def parse_url(url: str, invert: bool = False) -> Dict[str, str]:
    '''Splits the URL into parts and converts them into a kebab-case view.'''
    parsed_url = urlparse(os.path.normcase(url))
    url_map = {
        'scheme': parsed_url.scheme,
        'netloc': parsed_url.netloc,
        'path': os.path.splitext(parsed_url.path)[0],
        'ext': os.path.splitext(parsed_url.path)[1],
        'params': parsed_url.params,
        'query': parsed_url.query,
        'fragment': parsed_url.fragment
    }
    if invert is True:
        url_map = {_: invert_name(url_map, _) for _ in url_map}

    return url_map


def invert_name(initial_name: str, key: str) -> str:
    '''Converts part of a URL to a kebab case.'''
    processed_name = initial_name[key]
    if key == 'netloc':
        processed_name = re.sub(USER_PASSWORD, '', processed_name)
    if key == 'path':
        processed_name = os.path.normpath(processed_name)
    processed_name = re.sub(NOT_WORD, '-', processed_name)
    processed_name = re.sub(HYPHENS_AROUND, '', processed_name)

    inverted_name = processed_name

    return inverted_name
