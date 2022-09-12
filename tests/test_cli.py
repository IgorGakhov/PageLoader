import os
import subprocess

import pytest

from page_loader import cli


HELP_CLI_MESSAGE = [
    'usage: page-loader [-h] [--output DESTINATION] url_address',
    'Downloads the page from the network and puts it in the specified existing',
    'directory (default: working directory).',
    'positional arguments:', 'url_address           page being downloaded',
    'options:', '-h, --help            show this help message and exit',
    '--output DESTINATION  output directory (default:'
]


def test_help_command():
    exit_status = os.system('page-loader -h')
    assert exit_status == 0

    help_output = (subprocess.check_output("page-loader -h", shell=True)).decode('utf-8')
    help_output = [_.strip() for _ in help_output.split('\n') if _]
    is_correct_help_message = all([(_ in help_output) for _ in HELP_CLI_MESSAGE])
    assert is_correct_help_message


def test_cli_without_args():
    with pytest.raises(SystemExit) as error:
        cli.parse_arguments()()
    assert error.type == SystemExit
    assert error.value.code == 2
