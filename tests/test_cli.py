import os
import subprocess

import pytest

from page_loader import cli


def test_cli_without_args():
    with pytest.raises(SystemExit) as error:
        cli.parse_arguments()()
    assert error.type == SystemExit
    assert error.value.code == 2
