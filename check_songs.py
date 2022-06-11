# make sure all_songs.txt is valid
from pathlib import Path
import glob
from collections import Counter

def checkDupes(all_songs_file):
    with open(all_songs_file, 'r') as file:
        lines = list(map(lambda x: x.strip(), file))
    counter = Counter(lines)
    for k,v in counter.items():
        if v > 1:
            print(f'Duplicate: {v} appearances\n\t{k}')
            for i in range(v-1):
                lines.remove(k)
    return lines, counter

def checkRemoved(all_songs, vers):
    with open('missing_songs.txt', 'w') as file:
        for ver in vers:
            missing = []
            dirs = glob.glob(ver + '/*')
            for dir in dirs:
                song = Path(dir).name
                if song not in all_songs:
                    missing.append(song)
            missing.sort()
            # write
            file.write(f'####### {ver} ####### songs in folder but not in list\n')
            for song in missing:
                file.write(song + '\n')


def main(all_songs_file):
    # root = Path('.')
    with open(all_songs_file, 'r') as file:
        for line in file:
            songname = line.strip()
            folders = glob.glob('./*/' + glob.escape(songname))
            # folders = list(root.glob('*/' + songname))
            if len(folders) > 1:
                # print('Duplicates:\n\t' + '\n\t'.join(map(lambda x: str(x), folders)))
                print('Duplicates:\n\t' + '\n\t'.join(folders))
            if len(folders) == 0:
                print("Not found:\n\t" + songname)


if __name__ == '__main__':
    VERS = ["DDR A3", "DDR A20 PLUS", "DDR A20", "DDR A", "DDR 2014", "DDR 2013", "DDR X3", "DDR X2", "DDR X", "DDR SuperNOVA2", "DDR SuperNOVA", "DDR EXTREME", "DDR MAX2", "DDR MAX", "DDR 5th", "DDR 4th", "DDR 3rd", "DDR 2nd", "DDR"]
    all_songs_file = 'all_songs.txt'
    all_songs, counter = checkDupes(all_songs_file)
    checkRemoved(all_songs, VERS)
    main(all_songs_file)
