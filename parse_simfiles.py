from functools import reduce
import json
from pathlib import Path
import sys

from BPMRange import BPMRange
from SimfileRes import SimfileRes
from SimfileParser import SimfileParser


from simfile import timing
from simfile import notes

from simfile.notes import NoteData, count
from simfile.notes.timed import time_notes
from simfile.timing import Beat, TimingData
from simfile.timing.engine import TimingEngine

# A song is defined by the schema below
'''
title
titletranslit
song_length
resources       // filenames of resource files (no path included)
    simfile:        String
    jacket:         String
levels          // Levels of single/double charts
    single
        beginner:   Int
        easy:       Int
        medium:     Int
        mard:       Int
        challenge:  Int
    double
        beginner:   Int
        easy:       Int
        medium:     Int
        mard:       Int
        challenge:  Int
chart           // BPM/STOPS data
    per_chart = True/False (False -> inherit from song)

    bpm_range
    bpms
    stops

    beginner:
        bpm_range:  String
        bpms:       [BPM]
        stops:      [STOP]
    easy
    medium
    mard
    challenge
'''
def writeJSON(d, fname):
    with open(fname, 'w') as file:
        json.dump(d, file)

def processSimfile(simfile_path) -> tuple[dict, dict]: 
    parser = SimfileParser(simfile_path)
    song_data = parser.song_data
    chart_data = parser.chart_data
    levels_data = parser.levels_data
    return song_data, chart_data, levels_data

def resDictInFolder(data:list[dict], ver:str):
    folder = Path(ver)
    # dict containing resources for songs in folder
    with open('all_songs.txt','r') as file:
        songs = list(map(lambda line: line.strip(), file))
        
    for path in folder.glob('*/'):
        # skip version banner
        if not path.is_dir():
            continue

        if path.name not in songs:
            # print(f'Skipping {path.name}')
            continue

        # save dict
        res = SimfileRes(path)
        # skip duplicate title (e.g. Happy, ever snow)
        if res.name in map(lambda d: d['name'], data):
            continue

        d = {
            'resources': res.to_dict(),
            'version': ver, 
            'name': res.name
            }
        data.append(d)
    

def copyResourcesInFolder(data:list) -> None:
    import subprocess

    # copy resources, i.e. banners and simfiles
    for d in data:
        res = d['resources']
        # if res['simfile']:
        #     src = Path(d['version']) / Path(res['simfile']).stem / res['simfile']
        #     dst = Path('Resources/simfiles') / res['simfile']
        #     subprocess.Popen(['cp', '-f', str(src.absolute()), str(dst.absolute()) ])

        if res['jacket']:
            src = Path(d['version']) / Path(res['simfile']).stem / res['jacket']
            dst = Path('Resources/jackets') / res['jacket']
            subprocess.Popen(['cp', '-f', str(src.absolute()), str(dst.absolute()) ])

def addChartData(data: list) -> None:
    for d in data:
        res = d['resources']
        simfile_path = Path(d['version']) / Path(res['simfile']).stem / res['simfile']
        
        # song data
        song_d, chart_d, levels_d = processSimfile(str(simfile_path))

        # save dict
        d.update(song_d)
        d['levels'] = levels_d
        d['chart'] = chart_d

def main_ver(data, ver):
    resDictInFolder(data, ver)
    return data

def main(VERS):
    data = []
    for ver in VERS:
        main_ver(data, ver)
    print("Finished reading resources")

    if '-n' not in sys.argv:
        copyResourcesInFolder(data)
        print("Finished copying")

    addChartData(data)
    print("Finished processing chart data")

    if '-n' not in sys.argv:
        writeJSON(data, 'Resources/data.json')
        print("Finished writing data")

    return data

if __name__ == '__main__':
    VERS = ["DDR A3", "DDR A20 PLUS", "DDR A20", "DDR A", "DDR 2014", "DDR 2013", "DDR X3", "DDR X2", "DDR X", "DDR SuperNOVA2", "DDR SuperNOVA", "DDR EXTREME", "DDR MAX2", "DDR MAX", "DDR 5th", "DDR 4th", "DDR 3rd", "DDR 2nd", "DDR"]
    # VERS = ['DDR A', 'DDR A3']

    # res_data = resDictInFolder(VERS[0])
    # # copyResourcesInFolder(res)
    # chart_data, levels_data = chartDataInRes(res_data)

    if '-l' in sys.argv:
        print('Reading data from json file')
        with open('Resources/data.json', 'r') as file:
            data = json.load(file)
    else:
        data = main(VERS)

def findSong(data, title):
    out = []
    for i, d in enumerate(data):
        if title.lower() in d['title'].lower() or title.lower() in d['titletranslit'].lower():
            out.append(i)
    return out if out else None