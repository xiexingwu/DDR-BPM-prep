SHELL := /bin/zsh
VERS = "DDR A3" "DDR A20 PLUS" "DDR A20" "DDR A" "DDR 2014" "DDR 2013" "DDR X3" "DDR X2" "DDR X" "DDR SuperNOVA2" "DDR SuperNOVA" "DDR EXTREME" "DDR MAX2" "DDR MAX" "DDR 5th" "DDR 4th" "DDR 3rd" "DDR 2nd" "DDR"

## PYTHON
main: check_songs
	$(info ###### CONSIDER RUNNING: make load; AND CHECKING THE VARIABLE: data)
	python src/parse_courses.py
	python src/parse_simfiles.py

# check for duplicates, missing songs, etc.
check_songs:
	$(info ###### MAKE SURE all_songs.txt HAS ENDING NEW LINE)
	$(info ###### MAKE SURE YOU HAVE RUN THE FOLLOWING: make unzip)
	python src/check_songs.py

# load data.json to inspect data
load:
	python3 -i src/parse_simfiles.py -l

## MODERN pipeline
scrape:
	bash scripts/zenius_pack.sh 1509 A3
	bash scripts/zenius_pack.sh 1293 "A20 PLUS"
	bash scripts/zenius_pack.sh 1292 A20
	bash scripts/zenius_pack.sh 1148 A
	bash scripts/zenius_pack.sh 864 2014
	bash scripts/zenius_pack.sh 845 2013
	bash scripts/zenius_pack.sh 802 X3
	bash scripts/zenius_pack.sh 546 X2
	bash scripts/zenius_pack.sh 295 X
	bash scripts/zenius_pack.sh 77 SuperNOVA2
	bash scripts/zenius_pack.sh 1 SuperNOVA
	bash scripts/zenius_pack.sh 41 EXTREME
	bash scripts/zenius_pack.sh 31 MAX2
	bash scripts/zenius_pack.sh 40 MAX
	bash scripts/zenius_pack.sh 30 5th
	bash scripts/zenius_pack.sh 39 4th
	bash scripts/zenius_pack.sh 38 3rd
	bash scripts/zenius_pack.sh 32 2nd
	bash scripts/zenius_pack.sh 37 1st

## LEGACY pipeline

# unzip data from ZiV zip files
unzip:
	bash scripts/unzip_pack.sh

# perform various file fixes
fix:
	bash scripts/fix.sh 

clean:
	mkdir -p log
	rm log/*.txt
