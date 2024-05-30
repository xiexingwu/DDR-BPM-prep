from pathlib import Path
import logging


dist_folder = Path("./DDR-BPM-assets")
seed_folder = Path("./data")
allsongs_file = str(seed_folder / "all_songs.txt")
removed_file = str(seed_folder / "removed.txt")
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
