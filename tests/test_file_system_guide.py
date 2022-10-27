from pathlib import Path

import pytest

from page_loader.load_processor.file_system_guide import \
    check_destination, make_resources_dir, get_file_path, get_dir_path
from page_loader.load_processor.name_converter import parse_url


@pytest.mark.parametrize('url, parsed_url', [
    (
        'http://example.com',
        {'scheme': 'http', 'netloc': 'example-com',
         'path': '', 'ext': '', 'params': '', 'query': '', 'fragment': ''}  # noqa: E501
    ),
    (
        'https://example.com/path1/path2',
        {'scheme': 'https', 'netloc': 'example-com',
         'path': 'path1-path2', 'ext': '', 'params': '', 'query': '', 'fragment': ''}  # noqa: E501
    ),
    (
        'https://example.com/path1/path2.html',
        {'scheme': 'https', 'netloc': 'example-com',
         'path': 'path1-path2', 'ext': 'html', 'params': '', 'query': '', 'fragment': ''}  # noqa: E501
    ),
    (
        'https://example.com/path1/path2.css',
        {'scheme': 'https', 'netloc': 'example-com',
         'path': 'path1-path2', 'ext': 'css', 'params': '', 'query': '', 'fragment': ''}  # noqa: E501
    ),
    (
        'https://login:password@example.com:80/path.php',
        {'scheme': 'https', 'netloc': 'example-com-80',
         'path': 'path', 'ext': 'php', 'params': '', 'query': '', 'fragment': ''}  # noqa: E501
    )
])
def test_parse_url(url, parsed_url):
    assert parse_url(url, invert=True) == parsed_url


@pytest.mark.parametrize('url, expected_file_path, \
    expected_file_path_with_custom_ext, expected_dir_path', [
    (
        'http://example.com',

        'example-com.html', 'example-com.ext', 'example-com_files'
    ),
    (
        'https://example.com',

        'example-com.html', 'example-com.ext',
        'example-com_files'
    ),
    (
        'https://example.com/',

        'example-com.html', 'example-com.ext',
        'example-com_files'
    ),
    (
        'https://example.com/path',

        'example-com-path.html', 'example-com-path.ext',
        'example-com-path_files'
    ),
    (
        'https://example.com/path1/path2',

        'example-com-path1-path2.html', 'example-com-path1-path2.ext',
        'example-com-path1-path2_files'
    ),
    (
        'https://example.com/path1/path2.css',

        'example-com-path1-path2.css', 'example-com-path1-path2.ext',
        'example-com-path1-path2_files'
    ),
    (
        'https://example.com/path?param1=value1&param2=value2',

        'example-com-path.html', 'example-com-path.ext',
        'example-com-path_files'
    ),
    (
        'https://example.com/path#anchor',

        'example-com-path.html', 'example-com-path.ext',
        'example-com-path_files'
    ),
    (
        'https://login:password@example.com:80/path.php',

        'example-com-80-path.php', 'example-com-80-path.ext',
        'example-com-80-path_files'
    ),
])
def test_get_paths(
    url, expected_file_path, expected_file_path_with_custom_ext,
    expected_dir_path, tmp_path: Path
):
    assert get_file_path(url, tmp_path) == \
        Path(tmp_path).joinpath(expected_file_path)
    assert get_file_path(url, tmp_path, ext='ext') == \
        Path(tmp_path).joinpath(expected_file_path_with_custom_ext)

    assert get_dir_path(url, tmp_path) == \
        Path(tmp_path).joinpath(expected_dir_path)


def test_for_unknown_directory():
    with pytest.raises(ValueError):
        check_destination('/fail/path/for/exit...')

    with pytest.raises(OSError):
        make_resources_dir('/fail/path/for/exit...')
