from typing import Final

import requests

from page_loader.logger import logger


GETTING_TEXT: Final[str] = 'Getting text from page {} ...'
GETTING_CONTENT: Final[str] = 'Getting content from page {} ...'
REQUEST: Final[str] = 'Content request at address {} ...'
RESPONSE: Final[str] = 'Response from page {} received.'
CONNECTION_ERROR: Final[str] = 'An error occurred connecting to page {}.'
REQUEST_ERROR: Final[str] = 'An ambiguous exception occurred while processing \
a request for page {}.\nMake sure your input is correct and try again later.'


def get_page_response(url: str) -> requests.Response:
    '''Gets the response to a page request.'''
    logger.debug(REQUEST.format(url))

    try:
        page = requests.get(url)
        if page.status_code == requests.codes.ok:
            logger.debug(RESPONSE.format(url))
            return page
        else:
            logger.error(CONNECTION_ERROR.format(url))
            raise requests.exceptions.ConnectionError

    except requests.exceptions.RequestException:
        logger.error(REQUEST_ERROR.format(url))
        raise requests.exceptions.RequestException


def load_page_text(url: str) -> str:
    '''Gets page.text from page.'''
    logger.debug(GETTING_TEXT.format(url))
    page = get_page_response(url)
    return page.text


def load_page_content(url: str) -> bytes:
    '''Gets page.content from page.'''
    logger.debug(GETTING_CONTENT.format(url))
    page = get_page_response(url)
    return page.content
