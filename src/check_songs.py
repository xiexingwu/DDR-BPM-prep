'''
make sure all_songs.txt is valid
'''
from __init__ import *

from pathlib import Path
import glob
from collections import Counter

INDENT = '\n\t'

def _findFileCaseSensitive(findIn: str, filename: str) -> tuple[list[str], list[str]]:
    files = glob.glob(findIn + glob.escape(filename))
    parents = set(Path(file).parent for file in files) 
    getFilenames = lambda p: map(lambda c: c.name, p.glob("*")) # get case-correct list of all files for a folder p
    valid_parents = set(filter(lambda parent: filename in getFilenames(parent), parents))
    return list(map(lambda p: str(p/filename), valid_parents)), list(map(lambda p: str(p), parents - valid_parents))

def _checkFiles(lines: list[str]) -> bool:
    flag = False
    for songname in lines:
        # folders = glob.glob('./DDR*/' + glob.escape(songname))
        folders, invalid_parents = _findFileCaseSensitive(findIn = './DDR*/', filename = songname)

        if len(folders) > 1:
            LOGGER.warning('Duplicates in files:' + INDENT + INDENT.join(folders))
        if len(folders) == 0:
            msg = "File not found:" + INDENT + songname
            if invalid_parents:
                msg += INDENT + "but found in " + ",".join(invalid_parents)
            LOGGER.error(msg)

            flag = True

    return flag

def _checkDupesInList(lines: list[str]) -> bool:
    flag = False
    counter = Counter(line.lower() for line in lines)
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
