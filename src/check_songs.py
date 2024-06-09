"""
make sure all_songs.txt is valid
"""

import env

from pathlib import Path
import glob
from itertools import chain
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
    for songname in lines:
        folders, invalid_parents = _findFileCaseSensitive(
            findIn=str(env.seed_dir) + "/**/", filename=songname
        )

        if len(folders) > 1:
            env.logger.warning("Duplicates in files:" + INDENT + INDENT.join(folders))
        if len(folders) == 0:
            msg = "File not found:" + INDENT + songname
            if invalid_parents:
                msg += INDENT + "but found in " + ",".join(invalid_parents)
            env.logger.error(msg)

            flag = True

    return flag


def _checkDupesInList(lines: list[str]) -> bool:
    flag = False
    counter = Counter(line.lower() for line in lines)
    for k, v in counter.items():
        if v > 1:
            flag = True
            env.logger.error(
                f"Duplicate: {v} appearances in {env.allsongs_file}" + INDENT + k
            )

    return flag


def _checkRemoved(lines: list[str]):
    """
    Shows songs in folders but not in env.allsongs_file or env.removed_file.
    This is probably since the songs have recently been removed from arcade.
    """
    import logging

    logger = env.logger.getChild("removed")
    logger.addHandler(logging.FileHandler(env.logfile("removed.txt")))
    logger.propagate = False

    # Open list of known removed songs
    with open(env.removed_file, "r") as file:
        known_removed = list(map(lambda x: x.strip(), file))

    invalid = set(known_removed) & set(lines)
    if invalid:
        env.logger.error(
            f"Following songs can only appear in one of '{env.allsongs_file}' and '{env.removed_file}':"
        )
        for i in invalid:
            env.logger.error(f"\t{i}")
        raise RuntimeError("Invalid song_list configuration")

    # check for folders that are suspected recently removed songs
    for ver_path in glob.glob(str(env.seed_dir / "*")):
        # only search within folders (not .zip)
        if Path(ver_path).is_file():
            continue

        removed = []
        song_path = chain(glob.glob(ver_path + "/*"), glob.glob(ver_path + "/.*"))
        for dir in song_path:
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
                f"{ver_path} - Suspected songs that are removed:"
                + INDENT
                + INDENT.join(removed)
            )
        else:
            logger.info(f"{ver_path} - No songs suspected as removed")


def main():
    error = False
    with open(env.allsongs_file, "r") as file:
        lines = list(map(lambda x: x.strip(), file))

    error |= _checkFiles(lines)
    error |= _checkDupesInList(lines)

    _checkRemoved(lines)

    if error:
        print(f"See {env.logfile()} for error")
        raise RuntimeError


if __name__ == "__main__":
    main()
