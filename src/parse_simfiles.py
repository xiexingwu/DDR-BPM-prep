from distutils.log import debug
from __init__ import *

import json
from pathlib import Path
import glob
import sys
from functools import reduce

from classes.SimfileRes import SimfileRes
from classes.SimfileParser import SimfileParser


def _writeJSON(d, fname) -> None:
    with open(fname, "w") as file:
        json.dump(d, file)

def _readJSON(fname: str) -> dict:
    with open(fname, "r") as file:
        d = json.load(file)
    return d

"""
load song file-info into "songs" in-place
"""
def loadSongs(songs:list[dict]) -> None:
    with open(ALLSONGS_FILE,"r") as file:
        titles = list(map(lambda line: line.strip(), file))
        
    for title in titles:
    # for path in folder.glob("*/"):
        folders = glob.glob("./DDR*/" + glob.escape(title))
        if not folders:
            LOGGER.error(f"{title} not found in files")
            raise RuntimeError

        if len(folders) > 1:
            LOGGER.warning(f"Duplicates ({len(folders)}): {title}")

        path = Path(folders.pop())
        # path.name should == song
        res = SimfileRes(path)

        # skip duplicate title (e.g. La bamba, Happy, ever snow)
        if res.name in map(lambda d: d["name"], songs):
            continue

        song = {
            "ssc": res.ssc,
            "version": path.parent.name, 
            "name": path.name
            }
        songs.append(song)
    

"""
loads stepchart data to "songs" in-place
"""
def addChartData(songs: list) -> None:
    for song in songs:
        simfile_path = Path(song["version"]) / song["name"] /  (song["name"] + (".ssc" if song["ssc"] else ".sm")) 
        
        parser = SimfileParser(simfile_path)

        # save dict
        song.update(parser.song_data)
        song["levels"] = parser.levels_data
        song["chart"] = parser.chart_data

"""
Copy simfiles & jackets to dist folder
"""
def copyFilesToDist(songs:list[dict]) -> None:
    import subprocess

    # copy resources, i.e. jackets and simfiles
    for song in songs:

        # Copy simfiles
        src = Path(song["version"]) / song["name"] / (song["name"] + (".ssc" if song["ssc"] else ".sm"))
        dst = SIMFILES_FOLDER / src.name
        subprocess.Popen(["cp", "-f", str(src.absolute()), str(dst.absolute()) ])

        # Copy Jackets
        src = Path(song["version"]) / song["name"] / (song["name"] + "-jacket.png")
        dst = JACKETS_FOLDER/ src.name
        subprocess.Popen(["cp", "-f", str(src.absolute()), str(dst.absolute()) ])

"""
Write basic info of all songs into a single file.
Use as an index to filter/sort/categorise songs.
"""
def writeSummaryToDist(songs):
    def flattenBpms(charts):
        if len(charts) == 1:
            return charts[0]["bpm_range"]
        bpms = [c["bpm_range"].split("~") for c in charts]
        min_bpm = str(reduce(min, [int(bpm[0]) for bpm in bpms]))
        max_bpm = str(reduce(max, [int(bpm[-1]) for bpm in bpms]))
        return min_bpm if min_bpm == max_bpm else '~'.join([min_bpm, max_bpm])

    def flattenLevels(levels):
        return [levels[diff] if diff in levels.keys() else 0 for diff in ["beginner", "easy", "medium", "hard", "challenge"]]
    
    summary = [{            
        "name": song["name"],
        "version": song["version"],
        "single": flattenLevels(song["levels"]["single"]),
        "double": flattenLevels(song["levels"]["double"]),
        "bpm_range": flattenBpms(song["chart"]),
    } for song in songs]

    _writeJSON(summary, str(DIST_FOLDER/"summary.json"))

def writeSongsToDist(songs):
    for song in songs:
        fname = song["name"] + ".json"
        _writeJSON(song, str(DATA_FOLDER/fname))
        LOGGER.debug(f"Wrote {fname}")

def main():
    songs = []
    loadSongs(songs)
    LOGGER.info("Finished loading resources")

    addChartData(songs)
    LOGGER.info("Finished processing chart data")

    if "-n" not in sys.argv:
        writeSummaryToDist(songs)
        LOGGER.info("Finished writing songs summary")
        writeSongsToDist(songs)
        LOGGER.info("Finished writing json data")
        copyFilesToDist(songs)
        LOGGER.info("Finished copying resources")

    return songs

"""
Utility Functions for interactive mode
"""
"""
Load previously generated data instead of parsing from scratch
"""
def _loadExistingData():
    files = glob.glob(str(DATA_FOLDER / "*.json"))
    data = [_readJSON(file) for file in files]
    return data

"""
Search for a song by name and get its index.
If the name is not an exact match, returns indices of all songs containing the substring
"""
def locSong(songs, title):
    out = []
    src = title.lower()
    for i, d in enumerate(songs):
        tgt1 = d["title"].lower()
        tgt2 = d["titletranslit"].lower()
        if src == tgt1 or src == tgt2:
            return [i]
        if src in tgt1 or src in tgt2:
            out.append(i)
    return out


if __name__ == "__main__":
    if "-l" in sys.argv:
        LOGGER.info("Reading data from json file")
        songs = _loadExistingData()
    else:
        songs = main()

