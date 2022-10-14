from typing import Final

import requests

from page_loader.logger import logger


REQUEST: Final[str] = 'Content request at address {} ...'
RESPONSE: Final[str] = 'Response from page {} received.'
CONNECTION_ERROR: Final[str] = 'An error occurred connecting to page {}.'
REQUEST_ERROR: Final[str] = 'An ambiguous exception occurred while processing \
a request for page {}.\nMake sure your input is correct and try again later.'


def get_response_content(url: str) -> requests.Response:
    '''Gets the response to a page request.'''
    logger.debug(REQUEST.format(url))

    try:
        page = requests.get(url)
        if page.status_code == requests.codes.ok:
            logger.debug(RESPONSE.format(url))
            is_text = 'text/' in page.headers['content-type']
            return page.text if is_text else page.content
        else:
            logger.error(CONNECTION_ERROR.format(url))
            raise requests.exceptions.ConnectionError

    except requests.exceptions.RequestException:
        logger.error(REQUEST_ERROR.format(url))
        raise requests.exceptions.RequestException
