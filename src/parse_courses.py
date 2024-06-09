import env
import utils
from build_tools import writeCourseToDist


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
        chunks.append(chunk)  # last course

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

    fillCourseInfo(sp, summary)
    fillCourseInfo(dp, summary, isSp=False)
    fillCourseInfo(ddr, summary)
    fillCourseInfo(l4, summary)

    dan_names = [
        "1st Dan (初段)",
        "2nd Dan (二段)",
        "3rd Dan (三段)",
        "4th Dan (四段)",
        "5th Dan (五段)",
        "6th Dan (六段)",
        "7th Dan (七段)",
        "8th Dan (八段)",
        "9th Dan (九段)",
        "10th Dan (十段)",
        "Kaiden (皆伝)",
    ]
    for i, name in enumerate(dan_names):
        sp[i].update({"name": name})
        dp[i].update({"name": name})

    writeCourseToDist(sp, "dan_sp")
    writeCourseToDist(dp, "dan_dp")
    writeCourseToDist(ddr, "ddr")
    writeCourseToDist(l4, "life4")
    return sp, dp, ddr, l4


if __name__ == "__main__":
    sp, dp, ddr, l4 = main()
