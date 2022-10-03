import os
import pathlib

import pytest

from page_loader.loading_handler.file_system_guide import *


@pytest.mark.parametrize('url, parsed_url', [
    (
        'http://example.com',
        {'scheme': 'http', 'netloc': 'example-com',
        'path': '', 'ext': '', 'params': '', 'query': '', 'fragment': ''}
    ),
    (
        'https://example.com/path1/path2',
        {'scheme': 'https', 'netloc': 'example-com',
        'path': 'path1-path2', 'ext': '', 'params': '', 'query': '', 'fragment': ''}
    ),
    (
        'https://example.com/path1/path2.html',
        {'scheme': 'https', 'netloc': 'example-com',
        'path': 'path1-path2', 'ext': 'html', 'params': '', 'query': '', 'fragment': ''}
    ),
    (
        'https://example.com/path1/path2.css',
        {'scheme': 'https', 'netloc': 'example-com',
        'path': 'path1-path2', 'ext': 'css', 'params': '', 'query': '', 'fragment': ''}
    ),
    (
        'https://login:password@example.com:80/path.php',
        {'scheme': 'https', 'netloc': 'example-com-80',
        'path': 'path', 'ext': 'php', 'params': '', 'query': '', 'fragment': ''}
    )
])
def test_parse_url(url, parsed_url):
    assert parse_url(url) == parsed_url


@pytest.mark.parametrize('url, expected_file_path, expected_dir_path,\
    expected_file_path_with_custom_ext, expected_dir_path_with_custom_ext', [
    (
        'http://example.com',

        'example-com.html', 'example-com_files', 'example-com.ext', 'example-com_ext'
    ),
    (
        'https://example.com',

        'example-com.html', 'example-com_files', 'example-com.ext', 'example-com_ext'
    ),
    (
        'https://example.com/',

        'example-com.html', 'example-com_files', 'example-com.ext', 'example-com_ext'
    ),
    (
        'https://example.com/path',

        'example-com-path.html', 'example-com-path_files', 'example-com-path.ext', 'example-com-path_ext'
    ),
    (
        'https://example.com/path1/path2',

        'example-com-path1-path2.html', 'example-com-path1-path2_files', 'example-com-path1-path2.ext', 'example-com-path1-path2_ext'
    ),
    (
        'https://example.com/path1/path2.css',

        'example-com-path1-path2.css', 'example-com-path1-path2_files', 'example-com-path1-path2.ext', 'example-com-path1-path2_ext'
    ),
    (
        'https://example.com/path?param1=value1&param2=value2',

        'example-com-path.html', 'example-com-path_files', 'example-com-path.ext', 'example-com-path_ext'
    ),
    (
        'https://example.com/path#anchor',

        'example-com-path.html', 'example-com-path_files', 'example-com-path.ext', 'example-com-path_ext'
    ),
    (
        'https://login:password@example.com:80/path.php',

        'example-com-80-path.php', 'example-com-80-path_files', 'example-com-80-path.ext', 'example-com-80-path_ext'
    ),
])
def test_get_paths(url, expected_file_path, expected_dir_path,\
    expected_file_path_with_custom_ext, expected_dir_path_with_custom_ext, tmp_path: pathlib.Path):

    assert get_file_path(url, tmp_path) == os.path.join(tmp_path, expected_file_path)
    assert get_file_path(url, tmp_path, ext='ext') == os.path.join(tmp_path, expected_file_path_with_custom_ext)

    assert get_dir_path(url, tmp_path) == os.path.join(tmp_path, expected_dir_path)
    assert get_dir_path(url, tmp_path, ext='ext') == os.path.join(tmp_path, expected_dir_path_with_custom_ext)


def test_for_unknown_directory():
    with pytest.raises(ValueError):
        get_file_path('https://www.google.ru/', '/fail/path/for/exit...')

    with pytest.raises(OSError):
        get_dir_path('https://www.google.ru/', '/fail/path/for/exit...')
