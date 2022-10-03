import os
import re
from urllib.parse import urlparse
from typing import Final, Optional, Dict

from page_loader.logger import DIRECTORY_CREATION_ERROR


DEFAULT_DIR: Final[str] = os.getcwd()

HTML_EXT: Final[str] = 'html'
DIR_EXT: Final[str] = 'files'

USER_PASSWORD: Final[re.Pattern] = re.compile(r'.*@')  # for Network location
NOT_WORD: Final[re.Pattern] = re.compile(r'\W')
HYPHENS_AROUND: Final[re.Pattern] = re.compile(r'(^-*)|(-*$)')


def get_file_path(url: str, destination: str, ext: Optional[str] = None) -> str:  # noqa: E501
    '''
    Description:
    ---
        Generates the full path of the file to save the page.

    Parameters:
    ---
        - url (str): Page being downloaded.
        - destination (str): Output directory.
        ---
        - ext (str): Saved file extension
        (by default - the original file extension, if not - '*.html').

    Return:
    ---
        file_path (str): Full path to the downloaded file.
    '''
    check_path_exists(destination)

    base_name = get_base_name(url)
    if ext is None:
        native_ext = parse_url(url).get('ext')
        ext = native_ext if native_ext else HTML_EXT

    file_name = f'{base_name}.{ext}'
    file_path = os.path.join(destination, file_name)

    return file_path


def get_dir_path(url: str, destination: str, ext: Optional[str] = None) -> str:
    '''
    Description:
    ---
        Generates the full path of the resources folder to save the resources.

    Parameters:
    ---
        - url (str): Page being downloaded.
        - destination (str): Output directory.
        ---
        - ext (str): Saved folder extension
        (by default - the original folder extension, if not - '*_files').

    Return:
    ---
        dir_path (str): Full path to the downloaded resources folder.
    '''
    dir_name = get_dir_name(url, ext)
    dir_path = os.path.join(destination, dir_name)

    check_path_exists(dir_path)

    return dir_path


def check_path_exists(destination: str) -> None:
    '''Checks if the path exists. If not, it creates it.'''
    if not os.path.exists(destination):
        try:
            os.makedirs(destination)
        except OSError:
            raise OSError(DIRECTORY_CREATION_ERROR.format(destination))


def get_dir_name(url: str, ext: Optional[str] = None) -> str:
    '''Generates a name for the resource directory.'''
    base_name = get_base_name(url)
    ext = DIR_EXT if ext is None else ext

    dir_name = f'{base_name}_{ext}'

    return dir_name


def get_base_name(url: str) -> str:
    '''Generates a base name for datastores.'''
    url_map = parse_url(url)

    netloc = url_map['netloc']
    path = '-' + url_map['path'] if url_map['path'] else ''

    return netloc + path


def parse_url(url: str) -> Dict[str, str]:
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
