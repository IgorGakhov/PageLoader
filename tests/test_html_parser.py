import os
import pathlib

import pytest
import requests
import requests_mock

from page_loader.loading_handler.html_parser import *
from tests.auxiliary import *


def test_search_resources():
    with requests_mock.Mocker() as mock:
        mock.get(HTML_URL, text=read_file(SOURCE_PAGE))
        html = requests.get(HTML_URL).text
    html, resources = search_resources(html, HTML_URL)

    assert resources == RESOURCES
    assert html == read_file(HTML_FIXTURE)


@pytest.mark.parametrize('link, full_link', [
    ('/', 'https://page-loader.hexlet.repl.co/'),
    ('/frontend/layout.css', 'https://page-loader.hexlet.repl.co/frontend/layout.css'),
    ('/courses', 'https://page-loader.hexlet.repl.co/courses'),
    ('https://ru.hexlet.io/packs/js/runtime.js', 'https://ru.hexlet.io/packs/js/runtime.js')
])
def test_get_full_link(link, full_link):
    assert get_full_link(link, HTML_URL) == full_link


@pytest.mark.parametrize('link, is_local', [
    ('https://page-loader.hexlet.repl.co/', True),
    ('https://hexlet.repl.co/', False),
    ('https://page-loader.hexlet.css/', False),
    ('https://ru.hexlet.io/packs/js/runtime.js', False),
    ('https://test-loader.hexlet.repl.co/', False),
    ('https://page-loader.hexlet.project.co/', False),
    ('https://google.com', False),
    ('/courses', False),
    ('https://ru.hexlet.io/packs/js/runtime.js', False)
])
def test_is_local_link(link, is_local):
    assert is_local_link(link, HTML_URL) == is_local


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


def test_save_resources(tmp_path: pathlib.Path):
    save_resources(RESOURCES, tmp_path)

    for resource in RESOURCES:
        assert resource['name'] in os.listdir(tmp_path)
    assert len(os.listdir(tmp_path)) == 4
