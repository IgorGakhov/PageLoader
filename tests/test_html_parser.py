import pytest
import requests
import requests_mock

from page_loader.handler.html_parser import \
    replace_resources, get_full_link, is_local_link
from tests.auxiliary import read_file, \
    SOURCE_PAGE, HTML_URL, HTML_FIXTURE, RESOURCES


def test_replace_resources():
    with requests_mock.Mocker() as mock:
        mock.get(HTML_URL, text=read_file(SOURCE_PAGE))
        html = requests.get(HTML_URL).text
    html, resources = replace_resources(html, HTML_URL)

    assert resources == RESOURCES
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
