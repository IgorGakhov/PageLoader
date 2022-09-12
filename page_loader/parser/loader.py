import os
import re
from urllib.parse import urlparse

import requests


DEFAULT_DIR = os.getcwd()


def download(url_address: str, destination: str = DEFAULT_DIR) -> str:
    '''
    Description:
    ---
        Downloads a page from the network
        and puts it in the specified existing directory.

    Parameters:
    ---
        - url_address (str): Page being downloaded.

        - output (str): Output directory
        (by default, to the program launch directory).

    Return:
    ---
        file_path (str): Full path to the downloaded file.
    '''
    filename = create_filename(url_address)
    filepath = os.path.join(destination, filename)

    page = requests.get(url_address)
    content = page.text

    with open(filepath, 'w') as file:
        file.write(content)

    return filepath


def create_filename(url_address: str) -> str:
    '''Forms a name for the file to be saved.'''
    url_address = os.path.normcase(url_address)
    structure = urlparse(url_address)

    path = os.path.normpath(structure.path)
    path = re.sub(r'\..*', '', path)

    query = '-' + structure.query if structure.query else ''
    fragment = '-' + structure.fragment if structure.fragment else ''
    tail = query + fragment

    filename = structure.netloc + path + tail
    filename = re.sub(r'\W', '-', filename)
    filename = re.sub(r'-$', '', filename) + '.html'

    return filename
