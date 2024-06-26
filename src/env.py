from pathlib import Path
from os import getenv
import logging


build_dir = Path(getenv("BUILD_DIR") or "./build")
build_courses_dir = build_dir / "courses"
build_jackets_dir = build_dir / "jackets"
build_simfiles_dir = build_dir / "simfiles"
build_songs_dir = build_dir / "songs"
build_summaries_dir = build_dir / "summaries"
for folder in [
    build_dir,
    build_courses_dir,
    build_jackets_dir,
    build_songs_dir,
    build_simfiles_dir,
    build_summaries_dir,
]:
    if not folder.exists():
        folder.mkdir()

seed_dir = Path(getenv("SEED_DIR") or "./data")
allsongs_file = str(seed_dir / "all_songs.txt")
removed_file = str(seed_dir / "removed.txt")
title_map_file = str(seed_dir / "title_map.csv")
per_chart_bpm_file = str(seed_dir / "per_chart_bpm.txt")
dansp_courses_file = str(seed_dir / "dansp_courses.txt")
dandp_courses_file = str(seed_dir / "dandp_courses.txt")
ddr_courses_file = str(seed_dir / "ddr_courses.txt")
life4_courses_file = str(seed_dir / "life4_courses.txt")


log_folder = Path("./log")


def logfile(fname: str = "log.txt") -> str:
    return str(log_folder / fname)


logging.basicConfig(
    filename=logfile(),
    filemode="w",
    format="[%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
