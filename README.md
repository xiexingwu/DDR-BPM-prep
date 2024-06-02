# Quickstart
## Install
Runs on Python 3.11.4 on MacOS M1.

### System dependencies
- python-tk
    - `brew install python-tk`
- ICU
    - MacOS instructions
    ```shell
    # may need to install xcode to get clibs: `xcode-select --install`
    brew install pkg-config icu4c
    export PATH=/opt/homebrew/opt/icu4c/bin:$PATH
    export PATH=/opt/homebrew/opt/icu4c/sbin:$PATH
    export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/homebrew/opt/icu4c/lib/pkgconfig
    ```
- ImageMagick (pre-deployment)
    - `brew install imagemagick` (may also need `brew install ghostscript`)
    - https://imagemagick.org/script/download.php

### Python dependencies
```shell
poetry install
```

## Folder structure & Workflow
Rely on `Makefile` targets imported from `Makefiles/*.mk` for the 3 main steps of the workflow:
1. Scraper

    Scrape the DDR simfiles from ZiV and unpack them to the seed folder (`./data/`).
    Misc. fixes are applied to the simfiles at this stage to make it easier for later stages.

2. Parser

    This is the set of python scripts that does most of the heavy lifting.
    Simfiles are parsed and summarised into various formats for convenience.

3. Deploy

    This stage focuses on building the remaining artefacts and deploying them.
    At the moment, deployment just means pushing the build artefacts to GH, 
    though this may change in the future if it becomes sufficiently inconvenient.

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

### Build for deployment
```shell
make predeploy
```

# Quality of Life
- Use `ipdb.set_trace()` for debugging.
- Use `ptpython` for a better REPL (see [official repo](https://github.com/prompt-toolkit/ptpython?tab=readme-ov-file#embedding-the-repl) on setting up a PYTHONSTARTUP).

# Improvements Ideas
- Automate scraping simfiles
    - maintain list of categoryid (one for each DDR version)
        - Example: A3 GET `https://zenius-i-vanisher.com/v5.2/download.php?type=ddrpack&categoryid=1509`)
    - Check response header:
        - Example: 302 Found `Location: ../zip/pack_1509_3038f1.zip`     
    - maintain list of downloaded filenames (probably unique?)
    - maintain list of deprecated song-titles
