import os
import logging
import logging.config
from typing import Dict, Final


CONSOLED_FORMAT: Final[str] = '{asctime} {levelname}: {message}'
CONSOLED_DATE_FORMAT: Final[str] = '%H:%M:%S'
DETAILED_FORMAT: Final[str] = '{asctime} - {filename}:{funcName}:{lineno} - \
{processName}: {process} | {threadName}: {thread}\n\
{name} {levelname}: {message}\n'

BASE_DIR: Final[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqa: E501
LOG_FILE: Final[str] = 'journal.log'

# Build paths inside the project like this: os.path.join(BASE_DIR, LOG_FILE)
LOCAL_LOG_PATH: Final[str] = os.path.join(BASE_DIR, LOG_FILE)


LOGGING: Final[Dict] = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'consoled': {
            'format': CONSOLED_FORMAT,
            'datefmt': CONSOLED_DATE_FORMAT,
            'style': '{'
        },
        'detailed': {
            'format': DETAILED_FORMAT,
            'style': '{'
        }
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'consoled'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': LOCAL_LOG_PATH
        }
    },

    'loggers': {
        'PageLoader': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('PageLoader')
