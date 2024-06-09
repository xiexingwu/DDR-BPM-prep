import env
import utils


def parseSongNameWithDiff(line):
    """Examples:
    D Song Name
    E Song Name
    """
    diff, name = line.split(" ", maxsplit=1)
    return {"diff": diff, "name": name}


def parseDanCourse(chunk):
    """Format:
    Course Name
    D Song Name
    E Song Name
    C Song Name
    """
    return {
        "songs": [parseSongNameWithDiff(line) for line in chunk],
    }


def parseDdrCourse(chunk):
    return {
        "name": chunk[0],
        "songs": [{"name": name} for name in chunk[1:]],
    }


def parseLife4Course(chunk):
    return {
        "name": chunk[0],
        "level": int(chunk[1]),
        "songs": [parseSongNameWithDiff(line) for line in chunk[2:]],
    }


def parseCourseFile(filename: str) -> dict:
    """Assumes files are chunks of text split by empty line"""
    chunks = []
    with open(filename, "r") as file:
        chunk = []
        for line in file:
            if stripped := line.strip():
                chunk.append(stripped)
            else:
                chunks.append(chunk)
                chunk = []

    return chunks


def fillCourseInfo(courses, summary, isSp: bool = True):
    for course in courses:
        for song in course["songs"]:
            env.logger.info(f"Searching for {song['name']}")
            smry = summary[utils.locSong(summary, song["name"], key="name")[0]]

            # title info
            song["title"] = smry["title"]

            # level info
            spDp = "sp" if isSp else "dp"
            song["level"] = {spDp: smry[spDp]}
            if "diff" in song.keys():
                diff = song["diff"]
                song["level"] = {diff: smry[spDp][diff]}

            # bpm
            song["bpm_range"] = smry["bpm_range"]


def main():

    summary = utils.readJson(str(env.build_summaries_dir / "summary.json"))

    sp = [parseDanCourse(chunk) for chunk in parseCourseFile(env.dansp_courses_file)]
    dp = [parseDanCourse(chunk) for chunk in parseCourseFile(env.dandp_courses_file)]
    ddr = [parseDdrCourse(chunk) for chunk in parseCourseFile(env.ddr_courses_file)]
    l4 = [parseLife4Course(chunk) for chunk in parseCourseFile(env.life4_courses_file)]

    sp = fillCourseInfo(sp, summary)
    dp = fillCourseInfo(sp, summary, isSp=False)
    ddr = fillCourseInfo(sp, summary)
    l4 = fillCourseInfo(sp, summary)
    return sp, dp, ddr, l4


if __name__ == "__main__":
    try:
        sp, dp, ddr, l4 = main()
    except:
        import ipdb
        import traceback
        import sys

        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
