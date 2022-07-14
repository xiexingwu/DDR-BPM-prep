from distutils.log import debug
from __init__ import *

import json
from pathlib import Path
import glob
import sys

from classes.SimfileRes import SimfileRes
from classes.SimfileParser import SimfileParser


def _writeJSON(d, fname):
    with open(fname, 'w') as file:
        json.dump(d, file)

def _readJSON(fname):
    with open(fname, 'r') as file:
        d = json.load(file)
    return d

def loadResources(data:list[dict]):
    with open(ALLSONGS_FILE,'r') as file:
        songs = list(map(lambda line: line.strip(), file))
        
    for song in songs:
    # for path in folder.glob('*/'):
        folders = glob.glob('./DDR*/' + glob.escape(song))
        if not folders:
            LOGGER.error(f'{song} not found in files')
            raise RuntimeError

        if len(folders) > 1:
            LOGGER.warning(f'Duplicates ({len(folders)}): {song}')

        path = Path(folders.pop())
        # path.name should == song
        res = SimfileRes(path)

        # skip duplicate title (e.g. La bamba, Happy, ever snow)
        if res.name in map(lambda d: d['name'], data):
            continue

        d = {
            'ssc': res.ssc,
            'version': path.parent.name, 
            'name': path.name
            }
        data.append(d)
    

def copyResourcesInFolder(data:list) -> None:
    import subprocess

    # copy resources, i.e. jackets and simfiles
    for d in data:

        # Copy simfiles
        src = Path(d['version']) / d['name'] / (d['name'] + (".ssc" if d['ssc'] else ".sm"))
        dst = SIMFILES_FOLDER / src.name
        subprocess.Popen(['cp', '-f', str(src.absolute()), str(dst.absolute()) ])

        # Copy Jackets
        src = Path(d['version']) / d['name'] / (d['name'] + "-jacket.png")
        dst = JACKETS_FOLDER/ src.name
        subprocess.Popen(['cp', '-f', str(src.absolute()), str(dst.absolute()) ])

def addChartData(data: list) -> None:
    for d in data:
        simfile_path = Path(d['version']) / d['name'] /  (d['name'] + (".ssc" if d['ssc'] else ".sm")) 
        
        # song data
        parser = SimfileParser(simfile_path)

        # save dict
        d.update(parser.song_data)
        d['levels'] = parser.levels_data
        d['chart'] = parser.chart_data

def writeData(data):
    for d in data:
        fname = f"{d['name']}.json"
        _writeJSON(d, str(DATA_FOLDER/fname))
        LOGGER.debug(f"Wrote {fname}")

def main():
    data = []
    loadResources(data)
    LOGGER.info("Finished loading resources")

    addChartData(data)
    LOGGER.info("Finished processing chart data")

    if '-n' not in sys.argv:
        copyResourcesInFolder(data)
        LOGGER.info("Finished copying resources")
        writeData(data)
        LOGGER.info("Finished writing json data")

    return data

def _loadData():
    files = glob.glob(str(DATA_FOLDER / '*.json'))
    data = [_readJSON(file) for file in files]
    return data


if __name__ == '__main__':
    if '-l' in sys.argv:
        LOGGER.info('Reading data from json file')
        data = _loadData()
    else:
        data = main()

def findSong(data, title):
    out = []
    src = title.lower()
    for i, d in enumerate(data):
        tgt1 = d['title'].lower()
        tgt2 = d['titletranslit'].lower()
        if src == tgt1 or src == tgt2:
            return [i]
        if src in tgt1 or src in tgt2:
            out.append(i)
    return out