import env
import utils
import build_tools as build
from classes.SimfileRes import SimfileRes
from classes.SimfileParser import SimfileParser

from pathlib import Path
import glob
import sys


def loadSongs(songs: list[dict]) -> None:
    """
    load song file-info into "songs" in-place
    """
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


def addChartData(songs: list) -> None:
    """
    loads stepchart data to "songs" in-place
    """
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


def main():
    songs = []
    loadSongs(songs)
    env.logger.info("Finished loading resources")

    addChartData(songs)
    env.logger.info("Finished processing chart data")

    if "-n" not in sys.argv:
        build.writeSongsToDist(songs)
        env.logger.info("Finished writing json data")
    return songs


if __name__ == "__main__":
    if "-l" in sys.argv:
        env.logger.info("Reading data from json file")
        files = glob.glob(str(env.dist_songs_folder / "*.json"))
        songs = [utils.readJson(file) for file in files]
        summary = utils.readJson(str(env.dist_summaries_folder / "summary.json"))
        songs_version = utils.readJson(
            str(env.dist_summaries_folder / "songs_version.json")
        )
        songs_level_sp = utils.readJson(
            str(env.dist_summaries_folder / "songs_level_sp.json")
        )
        songs_level_dp = utils.readJson(
            str(env.dist_summaries_folder / "songs_level_dp.json")
        )

    else:
        songs = main()

    if ("-l" not in sys.argv and "-n" not in sys.argv) or (
        "-l" in sys.argv and "-w" in sys.argv
    ):
        build.writeSummaryToDist(songs)
        env.logger.info("Finished writing songs summary")
        build.copyRawsToDist(songs)
        env.logger.info("Finished copying resources")

    if "-i" in sys.argv:
        from ptpython.repl import embed

        # Utility func
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

        sys.exit(embed(globals(), locals()))
