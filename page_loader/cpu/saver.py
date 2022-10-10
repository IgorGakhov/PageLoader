import os
from typing import List

from progress.bar import IncrementalBar

from page_loader.cpu.connector import get_response
from page_loader.logger import logger, \
    START_RESOURCES_SAVING, FINISH_RESOURCES_SAVING, \
    START_SAVE_RESOURCE, FINISH_SAVE_RESOURCE


def save_resources(resources: List, dir_path: str) -> None:
    '''Iterates through the passed list of resources,
    saves them locally at the given location.'''
    logger.debug(START_RESOURCES_SAVING)

    bar = IncrementalBar(
        'Resources Loading',
        max=len(resources),
        suffix='%(percent)d%%   [' + IncrementalBar.suffix + ']\n'
    )

    for resource in resources:

        link = resource['link']

        content = get_response(link).content
        path = os.path.join(dir_path, resource['name'])

        logger.debug(START_SAVE_RESOURCE.format(link, path))
        save(content, path, 'wb')
        logger.info(FINISH_SAVE_RESOURCE.format(link))

        bar.next()

    bar.finish()

    logger.debug(FINISH_RESOURCES_SAVING)


def save(content: str, path: str, mode='w') -> None:
    '''Writes a file in entered mode.'''
    with open(path, mode) as file:
        file.write(content)
