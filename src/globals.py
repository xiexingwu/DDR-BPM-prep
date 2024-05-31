from pathlib import Path
import logging


dist_folder = Path("./build")
dist_courses_folder = dist_folder / "courses"
dist_jackets_folder = dist_folder / "jackets"
dist_simfiles_folder = dist_folder / "simfiles"
dist_songs_folder = dist_folder / "songs"
dist_summaries_folder = dist_folder / "summaries"
for folder in [
    dist_folder,
    dist_courses_folder,
    dist_jackets_folder,
    dist_songs_folder,
    dist_simfiles_folder,
    dist_summaries_folder,
]:
    if not folder.exists():
        folder.mkdir()

seed_folder = Path("./data")
allsongs_file = str(seed_folder / "all_songs.txt")
removed_file = str(seed_folder / "removed.txt")
name_map_file = str(seed_folder / "name_map.csv")
ddr_courses_file = str(seed_folder / "ddr_courses.txt")
life4_courses_file = str(seed_folder / "life4_courses.txt")


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
