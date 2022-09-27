import os

import pytest

from page_loader import cli


def test_help_command():
    exit_status = os.system('page-loader -h')
    assert exit_status == 0


def test_cli_without_args():
    with pytest.raises(SystemExit) as error:
        cli.parse_arguments()()
    assert error.type == SystemExit
    assert error.value.code == 2
