import env
import utils

from pathlib import Path
from functools import reduce


def copyRawsToDist(songs: list[dict]) -> None:
    """
    Copy simfiles & jackets to dist folder
    """
    import subprocess

    # copy resources, i.e. jackets and simfiles
    for song in songs:

        # Copy simfiles
        src = (
            Path(env.seed_dir)
            / song["version"]
            / song["name"]
            / (song["name"] + (".ssc" if song["ssc"] else ".sm"))
        )
        dst = env.build_simfiles_dir / src.name
        subprocess.Popen(["cp", "-f", str(src.absolute()), str(dst.absolute())])

        # Copy Jackets
        src = (
            Path(env.seed_dir)
            / song["version"]
            / song["name"]
            / (song["name"] + "-jacket.png")
        )
        dst = env.build_jackets_dir / src.name
        subprocess.Popen(["cp", "-f", str(src.absolute()), str(dst.absolute())])


def writeSongsToDist(songs):
    for song in songs:
        fname = song["name"] + ".json"
        env.logger.debug(f"Writing {fname}")
        utils.writeJson(song, str(env.build_songs_dir / fname))


def writeSummaryToDist(songs):
    """
    Write basic info of all songs into a single file.
    Use as an index to filter/sort/categorise songs.
    """

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
            "title": song["title"],
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
    songs_name = utils.sortSongsByTitle(summary)

    utils.writeJson(summary, str(env.build_summaries_dir / "summary.json"))
    utils.writeJson(
        songs_version, str(env.build_summaries_dir / "songs_version.json")
    )
    utils.writeJson(
        songs_level_sp, str(env.build_summaries_dir / "songs_level_sp.json")
    )
    utils.writeJson(
        songs_level_dp, str(env.build_summaries_dir / "songs_level_dp.json")
    )
    utils.writeJson(songs_name, str(env.build_summaries_dir / "songs_name.json"))
