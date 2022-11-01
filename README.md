# PageLoader
___

The training project "PageLoader" on the Python Development course on [Hexlet.io](https://ru.hexlet.io/programs/python).

[![Actions Status](https://github.com/IgorGakhov/python-project-51/workflows/hexlet-check/badge.svg)](https://github.com/IgorGakhov/python-project-51/actions) [![linter-and-tests-check](https://github.com/IgorGakhov/python-project-51/actions/workflows/linter-and-tests-check.yml/badge.svg?branch=main)](https://github.com/IgorGakhov/python-project-51/actions/workflows/linter-and-tests-check.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/ae0051d5e1631ad05334/maintainability)](https://codeclimate.com/github/IgorGakhov/python-project-51/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/ae0051d5e1631ad05334/test_coverage)](https://codeclimate.com/github/IgorGakhov/python-project-51/test_coverage)

### Built With
Languages, frameworks and libraries used in the implementation of the project:

[![](https://img.shields.io/badge/language-python-blue)](https://github.com/topics/python) [![](https://img.shields.io/badge/library-requests-%2399FFCC)](https://github.com/topics/requests) [![](https://img.shields.io/badge/library-beautifulsoup-%2311303D)](https://github.com/topics/beautifulsoup) [![](https://img.shields.io/badge/library-urllib.parse-%230000FF)](https://github.com/topics/urllib-parser) [![](https://img.shields.io/badge/library-re-orange)](https://github.com/topics/re) [![](https://img.shields.io/badge/library-os-%2399004C)](https://github.com/topics/os) [![](https://img.shields.io/badge/library-sys-%23000000)](https://github.com/topics/sys) [![](https://img.shields.io/badge/library-threading-%23CC00CC)](https://github.com/topics/threading) [![](https://img.shields.io/badge/library-progress-%23E0E0E0)](https://github.com/topics/progress) [![](https://img.shields.io/badge/library-logging-%232B2F2F)](https://github.com/topics/logging) [![](https://img.shields.io/badge/library-traceback-%23CC0000)](https://github.com/topics/traceback) [![](https://img.shields.io/badge/library-argparse-lightgrey)](https://github.com/topics/argparse)

### Dependencies
List of dependencies, without which the project code will not work correctly:
- python = "^3.8"
- requests = "^2.28.1"
- beautifulsoup4 = "^4.11.1"
- progress = "^1.6"

## Description
**PageLoader** is a command line utility that downloads pages from the Internet and saves them to your computer. Together with the page, it downloads all the resources (pictures, styles and js) making it possible to open the page without the Internet.

By the same principle, saving pages in the browser is arranged.

The utility multi-threadedly downloads resources and shows the progress for each resource in the terminal.

### Summary
* [Description](#description)
* [Installation](#installation)
  * [Python](#python)
  * [Poetry](#poetry)
  * [Project package](#project-package)
* [Usage](#usage)
  * [As external library](#as-external-library)
  * [As CLI tool](#as-cli-tool)
  * [Help](#help)
  * [Demo](#demo)
  * [Page loading](#pushpin-page-loading)
* [Development](#development)
  * [Dev Dependencies](#dev-dependencies)
  * [Project Organization](#project-organization)
  * [Useful commands](#useful-commands)
___

## Installation

### Python
Before installing the package, you need to make sure that you have Python version 3.8 or higher installed:

```bash
# Windows, Ubuntu, MacOS:
>> python --version # or python -V
Python 3.8.0+
```
:warning: If a command without a version does not work, specify the Python version explicitly: ```python3 --version```.

If you have an older version installed, update with the following commands:

```bash
# Windows:
>> pip install python --upgrade
# Ubuntu:
>> sudo apt-get upgrade python3.X
# MacOS:
>> brew update && brew upgrade python
# * X - version number to be installed
```

If you don't have Python installed, you can download and install it from [the official Python website](https://www.python.org/downloads/). If you are an Ubuntu or MacOS user, then it is better to do this procedure through package managers. Open a terminal and run the command for your operating system:

```bash
# Ubuntu:
>> sudo apt update
>> sudo apt install python3.X
# MacOS:
# https://brew.sh/index_ru.html
>> brew install python3.X
# * X - version number to be installed
```

:exclamation: The configuration of assemblies of different versions of operating systems can vary greatly from each other, which makes it impossible to write a common instruction. If you're running an OS other than the above, or you're having errors after the suggested commands, search [Stack Overflow](https://stackoverflow.com/) for answers, maybe someone else has come across them before you! Setting up the environment is not easy! :slightly_smiling_face:

### Poetry

The project uses the Poetry manager. Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. You can read more about this tool on [the official Poetry website](https://python-poetry.org/).

Poetry provides a custom installer that will install poetry isolated from the rest of your system by vendorizing its dependencies. This is the recommended way of installing poetry.

```bash
# Windows (WSL), Linux, MacOS:
>> curl -sSL https://install.python-poetry.org | python3 -
# Windows (Powershell):
>> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
# If you have installed Python through the Microsoft Store, replace "py" with "python" in the command above.
```

:warning: On some systems, ```python``` may still refer to Python 2 instead of Python 3. The Poetry Team suggests a ```python3``` binary to avoid ambiguity.

:warning: By default, Poetry is installed into a platform and user-specific directory:

* ```~/Library/Application Support/pypoetry``` on *MacOS*.
* ```~/.local/share/pypoetry``` on *Linux/Unix*.
* ```%APPDATA%\pypoetry``` on *Windows*.

If you wish to change this, you may define the $POETRY_HOME environment variable:

```bash
>> curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
```

Add Poetry to your PATH.

Once Poetry is installed and in your $PATH, you can execute the following:

```bash
>> poetry --version
```

### Project package

To work with the package, you need to clone the repository to your computer. This is done using the ```git clone``` command. Clone the project on the command line:

```bash
# clone via HTTPS:
>> git clone https://github.com/IgorGakhov/python-project-51.git
# clone via SSH:
>> git clone git@github.com:IgorGakhov/python-project-51.git
```

It remains to move to the directory and install the package:

```bash
>> cd python-project-51
>> poetry build
>> python3 -m pip install --user dist/*.whl
# If you have previously installed a package and want to update it, use the following command:
# >> python3 -m pip install --user --force-reinstall dist/*.whl
```

Finally, we can move on to using the project functionality!

___

## Usage

### As external library

```python
from page_loader import download
file_path = download(url_address, destination)
```

### As CLI tool

#### Help

The utility provides the ability to call the help command if you find it difficult to use:

```bash
>> page-loader --help
```
```bash
usage: page-loader [-h] [--output DESTINATION] url_address

Downloads the page from the network and puts it in the specified existing directory (default: working directory).

positional arguments:
  url_address           page being downloaded

options:
  -h, --help            show this help message and exit
  --output DESTINATION  output directory (default: current dir)
```
[![asciicast](https://asciinema.org/a/bMjVf7lsi1CJT7q2ZpXe2UcmU.svg)](https://asciinema.org/a/bMjVf7lsi1CJT7q2ZpXe2UcmU)

#### Demo

:zap: Only absolute file paths are supported.

##### :pushpin: Page loading

The utility downloads resources and shows the progress of each resource in the terminal.

**Example**:
```bash
>> page-loader --output /home/user/page_storage https://page-loader.hexlet.repl.co/
```
```bash
12:41:24 INFO: Initiated download of page https://page-loader.hexlet.repl.co/ to local directory «/home/user/page_storage» ...
12:41:25 INFO: Response from page https://page-loader.hexlet.repl.co/ received.
Page available for download!
Resources Loading |████████                        | 25%   [1/4]
12:41:26 INFO: [+] Resource https://page-loader.hexlet.repl.co/script.js saved successfully!
Resources Loading |████████████████                | 50%   [2/4]
12:41:26 INFO: [+] Resource https://page-loader.hexlet.repl.co/assets/professions/nodejs.png saved successfully!
Resources Loading |████████████████████████        | 75%   [3/4]
12:41:26 INFO: [+] Resource https://page-loader.hexlet.repl.co/assets/application.css saved successfully!
Resources Loading |████████████████████████████████| 100%   [4/4]
12:41:26 INFO: [+] Resource https://page-loader.hexlet.repl.co/courses saved successfully!

12:41:26 INFO: FINISHED! Loading is complete successfully!
The downloaded page is located in the «/home/user/page_storage/page-loader-hexlet-repl-co.html» file.

/home/user/page_storage/page-loader-hexlet-repl-co.html
```

[![asciicast](https://asciinema.org/a/gzaIYGrZVn4IGLIks45InJKIa.svg)](https://asciinema.org/a/gzaIYGrZVn4IGLIks45InJKIa)

___

## Development

### Dev Dependencies

List of dev-dependencies:
- flake8 = "^4.0.1"
- pytest = "^7.1.3"
- pytest-cov = "^3.0.0"
- requests-mock = "^1.10.0"

### Project Organization

```bash
>> tree .
```
```bash
.
├── page_loader
│   ├── __init__.py
│   ├── load_processor
│   │   ├── __init__.py
│   │   ├── downloader.py
│   │   ├── file_system_guide.py
│   │   ├── html_parser.py
│   │   ├── name_converter.py
│   │   ├── data_loader.py
│   │   └── saver.py
│   ├── cli.py
│   ├── logger.py
│   ├── progress.py
│   └── scripts
│       ├── __init__.py
│       └── run.py
└── tests
│   ├── auxiliary.py
│   ├── fixtures
│   │   ├── downloaded_nodejs_course.html
│   │   └── mocks
│   │       ├── assets-application.css
│   │       ├── assets-professions-nodejs.png
│   │       ├── courses.html
│   │       ├── packs-js-runtime.js
│   │       └── source_nodejs_course.html
│   ├── test_cli.py
│   ├── test_downloader.py
│   ├── test_file_system_guide.py
│   └── test_html_parser.py
├── journal.log
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
└── setup.cfg
```

### Useful commands

The commands most used in development are listed in the Makefile:

<dl>
    <dt><code>make package-install</code></dt>
    <dd>Installing a package in the user environment.</dd>
    <dt><code>make build</code></dt>
    <dd>Building the distribution of he Poetry package.</dd>
    <dt><code>make package-force-reinstall</code></dt>
    <dd>Reinstalling the package in the user environment.</dd>
    <dt><code>make lint</code></dt>
    <dd>Checking code with linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Tests the code.</dd>
    <dt><code>make fast-check</code></dt>
    <dd>Builds the distribution, reinstalls it in the user's environment, checks the code with tests and linter.</dd>
</dl>

___

**Thank you for attention!**

:man_technologist: Author: [@IgorGakhov](https://github.com/IgorGakhov)
