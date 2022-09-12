# !usr/bin/env python3


from typing import NoReturn

from page_loader.cli import parse_arguments
from page_loader.parser.loader import download


def main() -> NoReturn:
    """Run PageLoader script."""
    args = parse_arguments()
    print(download(args.url_address, args.destination))


if __name__ == '__main__':
    main()
