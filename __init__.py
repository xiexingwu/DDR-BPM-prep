from pathlib import Path

DIST_FOLDER = Path('./DDR-BPM-assets')
DATA_FOLDER = DIST_FOLDER/'data'
JACKETS_FOLDER = DIST_FOLDER/'jackets'
SIMFILES_FOLDER = DIST_FOLDER/'simfiles'

ALLSONGS_FILE = str(DIST_FOLDER/'all_songs.txt')
DDR_COURSES_FILE = str('ddr_courses.txt')
LIFE4_COURSES_FILE = str('life4_courses.txt')

VERS_FOLDERS = [
    "DDR A3", 
    "DDR A20 PLUS", 
    "DDR A20", 
    "DDR A", 
    "DDR 2014", 
    "DDR 2013", 
    "DDR X3", 
    "DDR X2", 
    "DDR X", 
    "DDR SuperNOVA2", 
    "DDR SuperNOVA", 
    "DDR EXTREME", 
    "DDR MAX2", 
    "DDR MAX", 
    "DDR 5th", 
    "DDR 4th", 
    "DDR 3rd", 
    "DDR 2nd", 
    "DDR"
]


LOG_FOLDER = Path('./log')
def LOGFILE(fname: str = 'log.txt') -> str:
    return str(LOG_FOLDER/fname)

import logging
logging.basicConfig(filename=LOGFILE(),
                    filemode='w',
                    format='[%(levelname)s] %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
