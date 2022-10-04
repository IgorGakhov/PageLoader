import requests

from page_loader.logger import logger, \
    REQUEST, RESPONSE, REQUEST_ERROR, CONNECTION_ERROR


def get_response(url: str) -> requests.Response:
    '''Gets the response to a page request.'''
    logger.debug(REQUEST.format(url))

    try:
        page = requests.get(url)
        if page.status_code == requests.codes.ok:
            logger.debug(RESPONSE.format(url))
            return page
        else:
            raise requests.exceptions.ConnectionError

    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError(CONNECTION_ERROR.format(url))
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(REQUEST_ERROR.format(url))
