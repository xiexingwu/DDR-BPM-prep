SHELL := /bin/zsh

################################################################################
# PYTHON Processor
################################################################################
main: check_songs
	$(info ################################################################################)
	$(info # Once finished, run `make load` to inspect the variable `songs`)
	$(info ################################################################################)
	poetry run python src/parse_courses.py
	poetry run python src/parse_simfiles.py
	# poetry run python -m ipdb -c continue src/parse_simfiles.py

# check for duplicates, missing songs, etc.
check_songs: clean
	$(info ################################################################################)
	$(info # 1. Make sure all_songs.txt has ending new line)
	$(info # 2. Make sure you ran a full scrape: make full_scrape)
	$(info ################################################################################)
	poetry run python src/check_songs.py

# load data & write
write:
	poetry run python src/parse_simfiles.py -l -w

# load data to inspect
load:
	poetry run python src/parse_simfiles.py -l -i

################################################################################
# SCRAPER
################################################################################
full_scrape: scrape_packs unzip scrape_songs dedupe fix 
scrape_packs:
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

# Some songs aren't located in the above packs.
# Download them into one of the folders
scrape_songs:
	bash scripts/zenius_song.sh 7568 2nd # PARANOiA KCET ~clean mix~
	bash scripts/zenius_song.sh 38006 3rd # LOVE THIS FEELIN'

# Some songs are duplicates
# Delete one version
dedupe:
	bash scripts/dedupe_song.sh "DYNAMITE RAVE" 3rd
	bash scripts/dedupe_song.sh "DYNAMITE RAVE (AIR Special)" SuperNOVA2
	bash scripts/dedupe_song.sh Happy X
	bash scripts/dedupe_song.sh "ever snow" MAX2
	bash scripts/dedupe_song.sh "La Bamba" EXTREME

unzip:
	bash scripts/unzip_pack.sh

# perform various file fixes
fix:
	bash scripts/fix.sh 


################################################################################
# CLEAN
################################################################################
clean:
	rm -fv log/*.txt || [ $$? -eq 1 ]

clobber: clean
	rm -fv data/**/*.zip
