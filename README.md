# Makefile `make` targets

## Improvements
- Automate scraping simfiles
    - maintain list of categoryid (one for each DDR version)
        - Example: A3 GET `https://zenius-i-vanisher.com/v5.2/download.php?type=ddrpack&categoryid=1509`)
    - Check response header:
        - Example: 302 Found `Location: ../zip/pack_1509_3038f1.zip`     
    - maintain list of downloaded filenames (probably unique?)
    - maintain list of deprecated song-titles

## Main
- `main`

    Fill in data for 
    - `jackets`, `data`, and `simfiles` folders
    - `courses.json`

- `load`

    Load the song data and enter Python interactive mode to inspect data.


- `check_songs`
    
    Check for duplicate/missing data etc.

## Utility
- `unzip`

    Unzip ZiV official arcade archives. Need to ensure the zip files are named as `DDR <VERSION>.zip`.

    The unzipped folders **SHOULD** automatically be renamed as `DDR <VERSION>/`.

- `fix` 

    Fix simfiles. For example, incorrect BPM in deltaMAX.

- `strip`

    Remove audio and video from `.zip` files to reduce storage space required.

# Files

- `src/check_songs.py`

    Check that all songs in `all_songs.txt` are generated

- `src/parse_simfiles.py`

    Parses the simfiles in all `'DDR */'` folders to generate the corresponding `json` files, which are subsequently used by DDR BPM.

- `src/parse_courses.py`

    Parses the following text files into `courses.json` for course data.

- `ddr_courses.txt`, `life4_courses.txt`

    List of courses in DDR and LIFE4. Difficulty of `-1` indicates variable difficulty.
