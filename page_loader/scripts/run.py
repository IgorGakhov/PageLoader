# !usr/bin/env python3


import sys
from typing import NoReturn

from page_loader.cli import parse_arguments
from page_loader.logger import logger, \
    PROGRAM_FAILURE
from page_loader.loading_handler.downloader import download


def main() -> NoReturn:
    """Run PageLoader script."""
    args = parse_arguments()
    try:
        print(download(args.url_address, args.destination))
    except RuntimeError:
        logger.critical(PROGRAM_FAILURE)
        sys.exit(1)


if __name__ == '__main__':
    main()
