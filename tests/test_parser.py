import os
import tempfile

import pytest
import requests
import requests_mock

from page_loader.parser import loader


@pytest.mark.parametrize('test_url, test_file, test_filename', [
    ('https://page-loader.hexlet.repl.co/',
    'tests/fixtures/nodejs_course.html',
    'page-loader-hexlet-repl-co.html')
])
def test_download(test_url, test_file, test_filename):    
    with requests_mock.Mocker() as mock, tempfile.TemporaryDirectory() as tmpdir:
        mock.get(test_url, text=open(test_file, 'r').read())

        received_path = loader.download(test_url, tmpdir)
        expected_path = os.path.join(tmpdir, test_filename)
        assert received_path == expected_path

        received_content = open(received_path, 'r').read()
        expected_content = requests.get(test_url).text
        assert received_content == expected_content


def test_convert_name():
    assert loader.create_filename('http://example.com') == 'example-com.html'
    assert loader.create_filename('https://example.com') == 'example-com.html'
    assert loader.create_filename('https://example.com/') == 'example-com.html'
    assert loader.create_filename('https://example.com/path') == 'example-com-path.html'
    assert loader.create_filename('https://example.com/path1/path2') == 'example-com-path1-path2.html'
    assert loader.create_filename('https://example.com/path1/path2.css') == 'example-com-path1-path2.html'
    assert loader.create_filename('https://example.com/path?param=value') == 'example-com-path-param-value.html'
    assert loader.create_filename('https://example.com/path?param1=value1&param2=value2') == 'example-com-path-param1-value1-param2-value2.html'
    assert loader.create_filename('https://example.com/path#anchor') == 'example-com-path-anchor.html'
    assert loader.create_filename('https://example.com/path?param1=value1&param2=value2#anchor/') == 'example-com-path-param1-value1-param2-value2-anchor.html'
