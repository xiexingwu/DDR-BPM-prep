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
        folders = glob.glob(str(env.seed_dir) + "/*/" + glob.escape(title))
        if not folders:
            env.logger.error(f"{title} not found in {env.seed_dir}")
            raise RuntimeError

        if len(folders) > 1:
            env.logger.warning(f"Duplicates ({len(folders)}): {title}")
            for folder in folders:
                env.logger.warning(f"\t{folder}")

        path = Path(folders.pop())
        res = SimfileRes(path)

        song = {"ssc": res.ssc, "version": path.parent.name, "name": path.name}
        songs.append(song)


def addChartData(songs: list) -> None:
    """
    loads stepchart data to "songs" in-place
    """
    for song in songs:
        simfile_path = (
            env.seed_dir
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
        files = glob.glob(str(env.build_songs_dir / "*.json"))
        songs = [utils.readJson(file) for file in files]
        summary = utils.readJson(str(env.build_summaries_dir / "summary.json"))
        songs_name = utils.readJson(str(env.build_summaries_dir / "songs_name.json"))
        songs_version = utils.readJson(
            str(env.build_summaries_dir / "songs_version.json")
        )
        songs_level_sp = utils.readJson(
            str(env.build_summaries_dir / "songs_level_sp.json")
        )
        songs_level_dp = utils.readJson(
            str(env.build_summaries_dir / "songs_level_dp.json")
        )
    else:
        songs = main()

    if ("-l" not in sys.argv and "-n" not in sys.argv) or (
        "-l" in sys.argv and "-w" in sys.argv
    ):
        build.writeSummaryToDist(songs)
        env.logger.info("Finished writing songs summary")

    if "-i" in sys.argv:
        from utils import locSong
        from ptpython.repl import embed

        sys.exit(embed(globals(), locals()))
