import env

import json
from pathlib import Path
import glob
import sys
from functools import reduce

from classes.SimfileRes import SimfileRes
from classes.SimfileParser import SimfileParser

import icu
import romkan
from unihandecode import Unihandecoder


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


def loadSongs(songs: list[dict]) -> None:
    with open(env.allsongs_file, "r") as file:
        titles = list(map(lambda line: line.strip(), file))

    for title in titles:
        # for path in folder.glob("*/"):
        folders = glob.glob(str(env.seed_folder) + "/*/" + glob.escape(title))
        if not folders:
            env.logger.error(f"{title} not found in {env.seed_folder}")
            raise RuntimeError

        if len(folders) > 1:
            env.logger.warning(f"Duplicates ({len(folders)}): {title}")
            for folder in folders:
                env.logger.warning(f"\t{folder}")

        path = Path(folders.pop())
        # path.name should == song
        res = SimfileRes(path)

        # skip duplicate title (e.g. La bamba, Happy, ever snow)
        if res.name in map(lambda d: d["name"], songs):
            continue

        song = {"ssc": res.ssc, "version": path.parent.name, "name": path.name}
        songs.append(song)


"""
loads stepchart data to "songs" in-place
"""


def addChartData(songs: list) -> None:
    for song in songs:
        simfile_path = (
            env.seed_folder
            / song["version"]
            / song["name"]
            / (song["name"] + (".ssc" if song["ssc"] else ".sm"))
        )

        parser = SimfileParser(simfile_path)

        # save dict
        song.update(parser.song_data)
        song.update(parser.levels_data)
        song["charts"] = parser.chart_data


"""
Copy simfiles & jackets to dist folder
"""


def copyRawsToDist(songs: list[dict]) -> None:
    import subprocess

    # copy resources, i.e. jackets and simfiles
    for song in songs:

        # Copy simfiles
        src = (
            Path(env.seed_folder)
            / song["version"]
            / song["name"]
            / (song["name"] + (".ssc" if song["ssc"] else ".sm"))
        )
        dst = env.dist_simfiles_folder / src.name
        subprocess.Popen(["cp", "-f", str(src.absolute()), str(dst.absolute())])

        # Copy Jackets
        src = (
            Path(env.seed_folder)
            / song["version"]
            / song["name"]
            / (song["name"] + "-jacket.png")
        )
        dst = env.dist_jackets_folder / src.name
        subprocess.Popen(["cp", "-f", str(src.absolute()), str(dst.absolute())])


"""
Write basic info of all songs into a single file.
Use as an index to filter/sort/categorise songs.
"""


def writeSummaryToDist(songs):

    def summarise(song):
        def summariseBpms(charts):
            bpms = [chart["bpm_range"].split("~") for chart in charts]
            min_bpm = reduce(min, [int(bpm[0]) for bpm in bpms])
            max_bpm = reduce(max, [int(bpm[-1]) for bpm in bpms])
            return [min_bpm] if min_bpm == max_bpm else [min_bpm, max_bpm]

        def summariseLevels(levels):
            map = {
                "beginner": "b",
                "easy": "B",
                "medium": "D",
                "hard": "E",
                "challenge": "C",
            }
            return {map[d]: levels[d] for d in map.keys() if d in levels.keys()}

        return {
            "name": song["name"],
            "version": song["version"],
            "sp": summariseLevels(song["sp"]),
            "dp": summariseLevels(song["dp"]),
            "bpm_range": summariseBpms(song["charts"]),
        }

    summary = [summarise(song) for song in songs]
    # Summary by version
    versions = [
        "A3",
        "A20 PLUS",
        "A20",
        "A",
        "2014",
        "2013",
        "X3",
        "X2",
        "X",
        "SuperNOVA2",
        "SuperNOVA",
        "EXTREME",
        "MAX2",
        "MAX",
        "5th",
        "4th",
        "3rd",
        "2nd",
        "1st",
    ]

    songs_version = {
        v: list(filter(lambda s: s["version"] == v, summary)) for v in versions
    }
    # Summary by level sp
    levels_sp = list(range(1, 20))
    songs_level_sp = {
        l: list(filter(lambda s: l in s["sp"].values(), summary)) for l in levels_sp
    }
    # Summary by level dp
    levels_dp = list(range(2, 20))
    songs_level_dp = {
        l: list(filter(lambda s: l in s["dp"].values(), summary)) for l in levels_dp
    }
    # Summary by name (see https://gist.github.com/ssut/4efb8870e8b5e9c07792)
    # songs_name = sortSongsByName(summary)

    _writeJSON(summary, str(env.dist_summaries_folder / "summary.json"))
    _writeJSON(songs_version, str(env.dist_summaries_folder / "songs_version.json"))
    _writeJSON(songs_level_sp, str(env.dist_summaries_folder / "songs_level_sp.json"))
    _writeJSON(songs_level_dp, str(env.dist_summaries_folder / "songs_level_dp.json"))


def sortSongsByName(songs):
    # Map weird song names, e.g. IX -> 9
    with open(env.name_map_file) as f:
        name_map = {old: new for old, new in map(lambda line: line.split(","), f)}

    names = set(song["name"] for song in songs)
    # jp_names =
    d = Unihandecoder(lang="ja")
    collator = icu.Collator.createInstance(icu.Locale("ja_JP.UTF-8"))
    corresponds = []
    for i, item in enumerate(names):
        kana = romkan.to_hiragana(d.decode(item))
        corresponds.append(kana)
    result = sorted(zip(names, corresponds), key=lambda x: collator.getSortKey(x[1]))
    return result


def translator(name):
    d = Unihandecoder(lang="ja")
    collator = icu.Collator.createInstance(icu.Locale("ja_JP.UTF-8"))
    kana = romkan.to_hiragana(d.decode(name))
    return kana


def writeSongsToDist(songs):
    for song in songs:
        fname = song["name"] + ".json"
        env.logger.debug(f"Writing {fname}")
        _writeJSON(song, str(env.dist_songs_folder / fname))


def main():
    songs = []
    loadSongs(songs)
    env.logger.info("Finished loading resources")

    addChartData(songs)
    env.logger.info("Finished processing chart data")

    if "-n" not in sys.argv:
        writeSongsToDist(songs)
        env.logger.info("Finished writing json data")
    return songs


"""
Utility Functions for interactive mode
"""


def locSong(songs, title):
    """
    Search for a song by name and get its index.
    If the name is not an exact match, returns indices of all songs containing the substring
    """
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
        env.logger.info("Reading data from json file")
        files = glob.glob(str(env.dist_songs_folder / "*.json"))
        songs = [_readJSON(file) for file in files]
        summary = _readJSON(str(env.dist_summaries_folder / "summary.json"))
        songs_version = _readJSON(str(env.dist_summaries_folder / "songs_version.json"))
        songs_level_sp = _readJSON(
            str(env.dist_summaries_folder / "songs_level_sp.json")
        )
        songs_level_dp = _readJSON(
            str(env.dist_summaries_folder / "songs_level_dp.json")
        )

    else:
        songs = main()

    if ("-l" not in sys.argv and "-n" not in sys.argv) or (
        "-l" in sys.argv and "-w" in sys.argv
    ):
        writeSummaryToDist(songs)
        env.logger.info("Finished writing songs summary")
        copyRawsToDist(songs)
        env.logger.info("Finished copying resources")

    if "-i" in sys.argv:
        from ptpython.repl import embed

        sys.exit(embed(globals(), locals()))
