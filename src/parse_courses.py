from __init__ import *

import json

DIFFICULTY = {
    'C' : 'Challenge',
    'E' : 'Expert',
    'D' : 'Difficult',
    'B' : 'Basic', 
    'b' : 'Beginner'
}

def parseDDRCourse(data):
    return {
        'name': data[0],
        'level': int(data[1]),
        'songs': [
            {'name': name} for name in data[2:]
            ],
        'source' : 'DDR'
    }

def parseLIFE4Course(data):
    return {
        'name': data[0],
        'level': int(data[1]),
        'songs': [
            {'name': name, 'difficulty': DIFFICULTY[diff]} for diff, name in zip(data[2], data[3:])
            ],
        'source' : 'LIFE4'
    }

def chunkBy(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def readCoursesFile(filename: str, source: str):
    txt = []
    with open(filename, 'r') as file:
        for line in file:
            if stripped := line.strip():
                txt.append(stripped)

    courses = []
    if source == 'DDR':
        for data in chunkBy(txt, 6):
            courses.append(parseDDRCourse(data))
    elif source == 'LIFE4':
        for data in chunkBy(txt, 7):
            courses.append(parseLIFE4Course(data))

    return courses

def main():
    d = []

    d += readCoursesFile(DDR_COURSES_FILE, source='DDR')
    d += readCoursesFile(LIFE4_COURSES_FILE, source='LIFE4')

    with open(str(RES_FOLDER/'courses.json'), 'w') as file:
        json.dump(d, file)
    return d


if __name__ == '__main__':
    d = main()
    