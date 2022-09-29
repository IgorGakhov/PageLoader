import os
import logging
import logging.config
from typing import Final, Dict


START_DOWNLOAD: Final[str] = 'Initiated download of page {} to local directory «{}» ...'  # noqa: E501
END_DOWNLOAD: Final[str] = '[FINISHED!] Loading is complete successfully!\n\
The downloaded page is located in the «{}» file,\n\
the resources are located in «{}».\n'
START_PARSING: Final[str] = 'Started HTML page parsing ...'
END_PARSING: Final[str] = 'Finished HTML page parsing.'
START_SEARCHING: Final[str] = 'Started replacing local resource links ...'
END_SEARCHING: Final[str] = 'Finished replacing local resource links.'
START_SAVING: Final[str] = 'Started saving page local resources ...'
END_SAVING: Final[str] = 'Finished saving page local resources.'
START_GET_RESOURCE: Final[str] = 'Resource content request at address {} ...'
END_GET_RESOURCE: Final[str] = 'Received resource content at address {}.'
START_SAVE_RESOURCE: Final[str] = 'Saving the resource {} along the path «{}» ...'  # noqa: E501
END_SAVE_RESOURCE: Final[str] = '[+] Resource {} saved successfully!'

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
