import os
import pathlib

import pytest

from page_loader.loading_handler.downloader import download
from tests.auxiliary import *


def test_download(tmp_path: pathlib.Path):

    # Проверка страницы...

    expected_path = os.path.join(tmp_path, HTML_NAME)
    received_path = download(HTML_URL, tmp_path)

    assert received_path == expected_path

    expected_content = read_file(HTML_FIXTURE)
    received_content = read_file(received_path)

    assert received_content == expected_content

    # Проверка ресурсов...

    resource_dir = os.path.join(tmp_path, DIRECTORY_NAME)

    assert os.path.exists(resource_dir)

    expected_css = read_file(CSS_FIXTURE, flag='r')
    received_css = read_file(os.path.join(resource_dir, CSS_NAME), flag='r')

    assert received_css == expected_css

    expected_inner_html = read_file(INNER_HTML_FIXTURE, flag='r')
    received_inner_html = read_file(os.path.join(resource_dir, INNER_HTML_NAME), flag='r')

    assert received_inner_html == expected_inner_html

    expected_image = read_file(IMAGE_FIXTURE, flag='rb')
    received_image = read_file(os.path.join(resource_dir, IMAGE_NAME), flag='rb')

    assert received_image == expected_image

    expected_js = read_file(JS_FIXTURE, flag='r')
    received_js = read_file(os.path.join(resource_dir, JS_NAME), flag='r')

    assert received_js == expected_js


def test_download_for_unknown_directory():
    with pytest.raises(SystemExit):
        download('https://www.google.ru/', '/fail/path/for/exit...')
