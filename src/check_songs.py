"""
make sure all_songs.txt is valid
"""

import globals

from pathlib import Path
import glob
from collections import Counter

INDENT = "\n\t"


def _findFileCaseSensitive(findIn: str, filename: str) -> tuple[list[str], list[str]]:
    files = glob.glob(findIn + glob.escape(filename))
    parents = set(Path(file).parent for file in files)
    getFilenames = lambda p: map(
        lambda c: c.name, p.glob("*")
    )  # get case-correct list of all files for a folder p
    valid_parents = set(
        filter(lambda parent: filename in getFilenames(parent), parents)
    )
    return list(map(lambda p: str(p / filename), valid_parents)), list(
        map(lambda p: str(p), parents - valid_parents)
    )


def _checkFiles(lines: list[str]) -> bool:
    flag = False
    search_glob = str(globals.seed_folder / "**") + "/"
    globals.logger.info(f"searching in {search_glob}")
    for songname in lines:
        folders, invalid_parents = _findFileCaseSensitive(
            findIn=search_glob, filename=songname
        )

        if len(folders) > 1:
            globals.logger.warning(
                "Duplicates in files:" + INDENT + INDENT.join(folders)
            )
        if len(folders) == 0:
            msg = "File not found:" + INDENT + songname
            if invalid_parents:
                msg += INDENT + "but found in " + ",".join(invalid_parents)
            globals.logger.error(msg)

            flag = True

    return flag


def _checkDupesInList(lines: list[str]) -> bool:
    flag = False
    counter = Counter(line.lower() for line in lines)
    for k, v in counter.items():
        if v > 1:
            flag = True
            globals.logger.error(
                f"Duplicate: {v} appearances in {globals.allsongs_file}" + INDENT + k
            )

    return flag


def _checkRemoved(lines: list[str]):
    """
    Shows songs in folders but not in globals.allsongs_file or globals.removed_file.
    This is probably since the songs have recently been removed from arcade.
    """
    import logging

    logger = globals.logger.getChild("removed")
    logger.addHandler(logging.FileHandler(globals.logfile("removed.txt")))
    logger.propagate = False

    # Open list of known removed songs
    with open(globals.removed_file, "r") as file:
        known_removed = list(map(lambda x: x.strip(), file))

    # check for folders that are suspected recently removed songs
    for folder in glob.glob(str(globals.seed_folder / "*")):
        # only search within folders (not .zip)
        if Path(folder).is_file():
            continue

        removed = []
        dirs = glob.glob(folder + "/*")
        for dir in dirs:
            # only check folders (not .png)
            if Path(dir).is_file():
                continue
            song = Path(dir).name
            if song not in lines and song not in known_removed:
                removed.append(song)
        removed.sort()

        # write suspects
        if removed:
            logger.info(
                f"{folder} - Suspected songs that are removed:"
                + INDENT
                + INDENT.join(removed)
            )
        else:
            logger.info(f"{folder} - No songs suspected as removed")

def main():
    error = False
    with open(globals.allsongs_file, "r") as file:
        lines = list(map(lambda x: x.strip(), file))

    error |= _checkFiles(lines)
    error |= _checkDupesInList(lines)

    _checkRemoved(lines)

    if error:
        print(f"See {globals.logfile()} for error")
        raise RuntimeError


if __name__ == "__main__":
    main()
