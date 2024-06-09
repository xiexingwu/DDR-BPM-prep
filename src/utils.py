import env

import json
from itertools import chain

import icu
import romkan
from unihandecode import Unihandecoder


def locSong(summary, title, *, key="title"):
    """
    Search for a song by key (default titletranslit) and get its index.
    If the name is not an exact match, returns indices of all songs containing the substring
    """
    out = []
    src = title.lower()
    for i, d in enumerate(summary):
        tgt = d[key].lower()
        if src == tgt:
            return [i]
        if src in tgt:
            out.append(i)
    return out


def writeJson(d, fname) -> None:
    with open(fname, "w") as file:
        json.dump(d, file)


def readJson(fname: str) -> dict:
    with open(fname, "r") as file:
        d = json.load(file)
    return d


def sortSongsByTitle(songs):
    """
    Partition songs into:
        あかさたなはまやらわABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
    Strategy:
        Split JP/EN titles
        Sort titles separately (keeping sort index)
        Partition the titles (doing the same with sort index)
        Use partitioned sort index to partition the songs (depends on dicts being ordered)
    """
    # Mapping for song titles that sort differently, e.g. IX -> 9
    with open(env.title_map_file) as f:
        title_map = {
            old: new for old, new in map(lambda line: line.strip().split(","), f)
        }

    # NOTE: From here on, `title` refers to the tuple (song_title, i)
    #   So expect most logic to be applied to title[0]
    titles = [
        (
            (
                title_map[song["title"]]
                if song["title"] in title_map.keys()
                else song["title"]
            ),
            i,
        )
        for i, song in enumerate(songs)
    ]

    # Split Japanese/English since they are sorted differently
    jp_titles = []
    en_titles = []
    for title in titles:
        # jp_title if first decoded char is not alphanumeric
        first_char = title[0][0]
        if first_char.isascii():
            en_titles.append(title)
        else:
            jp_titles.append(title)

    # Sort English A-Z0-9
    # TODO: Are symbols sorted separately?
    en_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    en_sorted = sorted(
        en_titles,
        key=lambda title: [
            en_alphabet.index(c) for c in title[0].upper() if c in en_alphabet
        ],
    )

    en_partitioned = [
        list(filter(lambda title: title[0][0].upper() == c, en_sorted))
        for c in en_alphabet
    ]

    # Translate Japanese to hiragana
    decoder = Unihandecoder(lang="ja")
    jp_kana = [
        (romkan.to_hiragana(decoder.decode(title[0])), title[1]) for title in jp_titles
    ]

    # Sort Japanese
    jp_collator = icu.Collator.createInstance(icu.Locale("ja_JP.UTF-8"))
    jp_sorted = sorted(
        jp_kana,
        key=lambda title: jp_collator.getSortKey(title[0]),
    )

    # Partition Japanese
    jp_alphabet = "あかさたなはまやらわ"
    jp_partitioned = [[] for kana in jp_alphabet]
    for title in jp_sorted:
        pos = sum(title[0][0] >= kana for kana in jp_alphabet) - 1
        assert pos >= 0
        assert pos < len(jp_alphabet)
        jp_partitioned[pos].append(title)

    # Apply partionining to songs via index (JP first, then EN)
    result = [
        {
            "category": char,
            "songs": list(map(lambda title: songs[title[1]], partitioned)),
        }
        for char, partitioned in zip(
            chain(jp_alphabet, en_alphabet), chain(jp_partitioned, en_partitioned)
        )
    ]
    return result
