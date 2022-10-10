import os
from pathlib import Path

import pytest
import requests
import requests_mock

from page_loader.cpu.downloader import download
from page_loader.cpu.connector import get_response
from page_loader.cpu.name_converter import create_resource_name
from page_loader.cpu.saver import save_resources
from tests.auxiliary import read_file, HTML_NAME, HTML_URL, HTML_FIXTURE, \
    DIRECTORY_NAME, CSS_NAME, CSS_FIXTURE, IMAGE_NAME, IMAGE_FIXTURE, \
    INNER_HTML_NAME, INNER_HTML_FIXTURE, JS_NAME, JS_FIXTURE, RESOURCES


def test_download(tmp_path: Path):

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
    received_inner_html = read_file(os.path.join(resource_dir, INNER_HTML_NAME), flag='r')  # noqa: E501

    assert received_inner_html == expected_inner_html

    expected_image = read_file(IMAGE_FIXTURE, flag='rb')
    received_image = read_file(os.path.join(resource_dir, IMAGE_NAME), flag='rb')  # noqa: E501

    assert received_image == expected_image

    expected_js = read_file(JS_FIXTURE, flag='r')
    received_js = read_file(os.path.join(resource_dir, JS_NAME), flag='r')

    assert received_js == expected_js


@pytest.mark.parametrize('link, resource_name', [
    (
        'https://page-loader.hexlet.repl.co/courses',
        'page-loader-hexlet-repl-co-courses.html'
    ),
    (
        'https://page-loader.hexlet.repl.co/assets/application.css',
        'page-loader-hexlet-repl-co-assets-application.css'
    ),
    (
        'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png',
        'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
    ),
    (
        'https://page-loader.hexlet.repl.co/script.js',
        'page-loader-hexlet-repl-co-script.js'
    )
])
def test_create_resource_name(link, resource_name):
    assert create_resource_name(link) == resource_name


def test_save_resources(tmp_path: Path):
    save_resources(RESOURCES, tmp_path)

    for resource in RESOURCES:
        assert resource['name'] in os.listdir(tmp_path)
    assert len(os.listdir(tmp_path)) == 4


def test_get_response_with_error_status():
    url = 'https://example.com'
    with requests_mock.Mocker() as m:
        m.get(url, status_code=404)
        with pytest.raises(requests.exceptions.RequestException):
            get_response(url)
