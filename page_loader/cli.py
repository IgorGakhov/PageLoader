import argparse

from page_loader.load_processor.downloader import DEFAULT_DIR


def parse_arguments() -> argparse.Namespace:
    """
    Description:
    ---
        Parse arguments for page-loader.

    Return:
    ---
        args (Namespace): Entered values.
    """
    parser = argparse.ArgumentParser(
        description='''Downloads the page from the network
        and puts it in the specified existing directory
        (default: working directory).'''
    )

    parser.add_argument(
        'url_address',
        help='page being downloaded',
        type=str
    )

    parser.add_argument(
        '-o', '--output',
        help=f'output directory (default: {DEFAULT_DIR})',
        dest='destination',
        default=DEFAULT_DIR,
        type=str
    )

    args = parser.parse_args()

    return args
