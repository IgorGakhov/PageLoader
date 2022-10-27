from pathlib import Path

import pytest
import requests
import requests_mock

from page_loader.load_processor.html_parser import \
    process_resources, get_full_link, is_local_link
from tests.auxiliary import read_file, \
    SOURCE_PAGE, HTML_URL, HTML_FIXTURE, DIRECTORY_NAME


def test_replace_resources(tmp_path: Path):
    with requests_mock.Mocker() as mock:
        mock.get(HTML_URL, text=read_file(SOURCE_PAGE))
        html = requests.get(HTML_URL).text
    dir_path = Path(tmp_path).joinpath(DIRECTORY_NAME)
    html, _ = process_resources(html, HTML_URL, dir_path)

    assert html == read_file(HTML_FIXTURE)


@pytest.mark.parametrize('link, full_link', [
    ('/', 'https://page-loader.hexlet.repl.co/'),
    ('/frontend/layout.css', 'https://page-loader.hexlet.repl.co/frontend/layout.css'),  # noqa: E501
    ('/courses', 'https://page-loader.hexlet.repl.co/courses'),
    ('https://ru.hexlet.io/packs/js/runtime.js', 'https://ru.hexlet.io/packs/js/runtime.js')  # noqa: E501
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
