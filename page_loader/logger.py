import os
import logging
import logging.config
from typing import Final, Dict


# DEBUG & INFO levels
START_DOWNLOAD: Final[str] = 'Initiated download of page {} \
to local directory «{}» ...'
FINISH_DOWNLOAD: Final[str] = 'FINISHED! Loading is complete successfully!\n\
The downloaded page is located in the «{}» file,\n'
START_PARSING: Final[str] = 'Started HTML page parsing ...'
FINISH_PARSING: Final[str] = 'Finished HTML page parsing.'
START_REQUEST: Final[str] = 'Getting a response from a page {} ...'
FINISH_REQUEST: Final[str] = 'Response from page {} received.\n\
Page available for download!'
START_SEARCHING: Final[str] = 'Started replacing local resource links ...'
FINISH_SEARCHING: Final[str] = 'Finished replacing local resource links.'
START_SAVING: Final[str] = 'Started saving page local resources ...'
FINISH_SAVING: Final[str] = 'Finished saving page local resources.'
START_GET_RESOURCE: Final[str] = 'Resource content request at address {} ...'
FINISH_GET_RESOURCE: Final[str] = 'Received resource content at address {}.'
START_SAVE_RESOURCE: Final[str] = 'Saving the resource {} \
along the path «{}» ...'
FINISH_SAVE_RESOURCE: Final[str] = '[+] Resource {} saved successfully!'

# ERROR level
PROGRAM_FAILURE: Final[str] = 'There was a crash at runtime \
for an unknown reason. See log file.'
DIRECTORY_CREATION_ERROR: Final[str] = 'A system error occurred \
while creating director(y/ies): «{}».'
CONNECTION_ERROR: Final[str] = 'An error occurred connecting to page {}.'
REQUEST_ERROR: Final[str] = 'An ambiguous exception occurred while processing \
a request for page {}.\nMake sure your input is correct and try again later.'

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
