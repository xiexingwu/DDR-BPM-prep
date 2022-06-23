'''
make sure all_songs.txt is valid
'''
from __init__ import *

from pathlib import Path
import glob
from collections import Counter

INDENT = '\n\t'


def _checkFiles(lines: list[str]) -> bool:
    flag = False
    for songname in lines:
        folders = glob.glob('./DDR*/' + glob.escape(songname))

        if len(folders) > 1:
            LOGGER.warning('Duplicates in files:' + INDENT + INDENT.join(folders))
        if len(folders) == 0:
            LOGGER.error("File not found:" + INDENT + songname)
            flag = True

    return flag

def _checkDupesInList(lines: list[str]) -> bool:
    flag = False
    counter = Counter(lines)
    for k,v in counter.items():
        if v > 1:
            flag = True
            LOGGER.error(f'Duplicate: {v} appearances in {ALLSONGS_FILE}' + INDENT + k)

    return flag

def _showRemoved(lines: list[str]):
    '''
    Shows songs in folders but not in ALLSONGS_FILE. 
    This is probably since the songs have been removed from arcade.
    '''
    import logging
    logger = LOGGER.getChild('removed')
    logger.addHandler(logging.FileHandler(LOGFILE('removed.txt')))
    logger.propagate = False
    for ver in VERS_FOLDERS:
        removed = []
        dirs = glob.glob(ver + '/*')
        for dir in dirs:
            song = Path(dir).name
            if song not in lines:
                removed.append(song)
        removed.sort()
        # write
        if removed:
            logger.info(f"{ver} songs in folder but not in list" + INDENT + INDENT.join(removed))


def main():
    error = False
    with open(ALLSONGS_FILE, 'r') as file:
        lines = list(map(lambda x: x.strip(), file))

    error |= _checkFiles(lines)
    error |= _checkDupesInList(lines)

    _showRemoved(lines)

    if error:
        print(f"See {LOGFILE()} for error")
        raise RuntimeError

if __name__ == '__main__':
    main()
