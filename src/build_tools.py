import env
import utils

from functools import reduce
from collections import Counter


def writeCourseToDist(course, name):
    fname = f"{name}.json"
    env.logger.debug(f"Writing {fname}")
    utils.writeJson(course, str(env.build_courses_dir / fname))


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

    with open(env.per_chart_bpm_file, "r") as f:
        title_bpm = list(map(lambda line: line.strip(), f))
        per_chart_bpm_range = {tb.split(",")[0]: tb.split(",")[1] for tb in title_bpm}

    def summarise(song):
        def parseChartBpm(chart):
            if (
                sum(isinstance(bpm, int) for bpm in chart["bpm_range"]) == 3
            ):  # array of 3 int
                return chart["bpm_range"]
            elif "~" in chart["bpm_range"]:
                return [int(bpm) for bpm in chart["bpm_range"].split("~")]
            else:
                return [int(chart["bpm_range"]) for _ in range(3)]

        def summariseBpms(charts):
            from statistics import mode

            bpms = [parseChartBpm(chart) for chart in charts]

            min_bpm = reduce(min, [int(bpm[0]) for bpm in bpms])
            dom_bpm = mode(int(bpm[1]) for bpm in bpms)
            max_bpm = reduce(max, [int(bpm[2]) for bpm in bpms])
            return [min_bpm] if min_bpm == max_bpm else [min_bpm, dom_bpm, max_bpm]

        def summariseLevels(levels):
            map = {
                "beginner": "b",
                "easy": "B",
                "medium": "D",
                "hard": "E",
                "challenge": "C",
            }
            return {map[d]: levels[d] for d in map.keys() if d in levels.keys()}

        song_summary = {
            "name": song["name"],
            "title": song["title"],
            "version": song["version"],
            "sp": summariseLevels(song["sp"]),
            "dp": summariseLevels(song["dp"]),
            "bpm_range": summariseBpms(song["charts"]),
        }

        if len(song["charts"]) == 5:
            assert song["name"] in per_chart_bpm_range
            i_diff = "bBDEC".index(per_chart_bpm_range[song["name"]])
            bpm_range = song["charts"][i_diff]["bpm_range"]

            song["per_chart"] = "".join(
                diff
                for chart, diff in zip(song["charts"], "bBDEC")
                if chart["bpm_range"] != bpm_range
            )

        return song_summary

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

    # Summary by name - do 1st so later summaries are secondary sorted by name
    songs_name = utils.sortSongsByTitle(summary)
    assert len(summary) == sum(len(partition["songs"]) for partition in songs_name)
    summary = [
        song
        for song in sum((songs_char["songs"] for songs_char in songs_name), start=[])
    ]

    # Summary by version
    songs_version = [
        {"category": v, "songs": list(filter(lambda s: s["version"] == v, summary))}
        for v in versions
    ]
    # Summary by level sp
    levels_sp = list(range(1, 20))
    songs_level_sp = [
        {"category": l, "songs": list(filter(lambda s: l in s["sp"].values(), summary))}
        for l in levels_sp
    ]
    # Summary by level dp
    levels_dp = list(range(2, 20))
    songs_level_dp = [
        {"category": l, "songs": list(filter(lambda s: l in s["dp"].values(), summary))}
        for l in levels_dp
    ]

    # Convert dicts to arrays since JSON is technically unordered

    utils.writeJson(summary, str(env.build_summaries_dir / "summary.json"))
    utils.writeJson(songs_version, str(env.build_summaries_dir / "songs_version.json"))
    utils.writeJson(
        songs_level_sp, str(env.build_summaries_dir / "songs_level_sp.json")
    )
    utils.writeJson(
        songs_level_dp, str(env.build_summaries_dir / "songs_level_dp.json")
    )
    utils.writeJson(songs_name, str(env.build_summaries_dir / "songs_name.json"))
