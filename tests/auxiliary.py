from typing import Final, List, Dict

SOURCE_PAGE: Final[str] = 'tests/fixtures/mocks/source_nodejs_course.html'
DIRECTORY_NAME: Final[str] = 'page-loader-hexlet-repl-co_files'

HTML_URL: Final[str] = 'https://page-loader.hexlet.repl.co/'
CSS_URL: Final[str] = 'https://page-loader.hexlet.repl.co/assets/application.css'  # noqa: E501
JS_URL: Final[str] = 'https://page-loader.hexlet.repl.co/script.js'
IMAGE_URL: Final[str] = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'  # noqa: E501
INNER_HTML_URL: Final[str] = 'https://page-loader.hexlet.repl.co/courses'

HTML_FIXTURE: Final[str] = 'tests/fixtures/downloaded_nodejs_course.html'
CSS_FIXTURE: Final[str] = 'tests/fixtures/mocks/assets-application.css'
JS_FIXTURE: Final[str] = 'tests/fixtures/mocks/packs-js-runtime.js'
IMAGE_FIXTURE: Final[str] = 'tests/fixtures/mocks/assets-professions-nodejs.png'  # noqa: E501
INNER_HTML_FIXTURE: Final[str] = 'tests/fixtures/mocks/courses.html'

HTML_NAME: Final[str] = 'page-loader-hexlet-repl-co.html'
CSS_NAME: Final[str] = 'page-loader-hexlet-repl-co-assets-application.css'
JS_NAME: Final[str] = 'page-loader-hexlet-repl-co-script.js'
IMAGE_NAME: Final[str] = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'  # noqa: E501
INNER_HTML_NAME: Final[str] = 'page-loader-hexlet-repl-co-courses.html'

RESOURCES: Final[List[Dict[str, str]]] = [
    {
        'link': 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png',  # noqa: E501
        'name': 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
    },
    {
        'link': 'https://page-loader.hexlet.repl.co/assets/application.css',
        'name': 'page-loader-hexlet-repl-co-assets-application.css'
    },
    {
        'link': 'https://page-loader.hexlet.repl.co/courses',
        'name': 'page-loader-hexlet-repl-co-courses.html'
    },
    {
        'link': 'https://page-loader.hexlet.repl.co/script.js',
        'name': 'page-loader-hexlet-repl-co-script.js'
    }
]


def read_file(file_path: str, flag: str = 'r') -> str:
    with open(file_path, flag) as file:
        return file.read()
