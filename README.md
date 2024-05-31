# Quickstart
## Install
Runs on Python 3.11.4 on MacOS M1.

### System dependencies
```
- python-tk
    - `brew install python-tk`
- ICU (MacOS instructions)
    - `brew install pkg-config icu4c`
    - `export PATH=/opt/homebrew/opt/icu4c/bin:$PATH`
    - `export PATH=/opt/homebrew/opt/icu4c/sbin:$PATH`
    - `export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/homebrew/opt/icu4c/lib/pkgconfig`
    - (may need to install xcode to get clibs) `xcode-select --install`
```

### Poetry
```
# install
poetry install
```

## Run
### Scrape
```shell
make full_scrape
```

### Process and write data
```shell
make main
```

### Load data to inspect
```shell
make load
```

# Improvements
- Automate scraping simfiles
    - maintain list of categoryid (one for each DDR version)
        - Example: A3 GET `https://zenius-i-vanisher.com/v5.2/download.php?type=ddrpack&categoryid=1509`)
    - Check response header:
        - Example: 302 Found `Location: ../zip/pack_1509_3038f1.zip`     
    - maintain list of downloaded filenames (probably unique?)
    - maintain list of deprecated song-titles
