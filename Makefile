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
	bash scripts/zenius_pack.sh 1509 # A3
	bash scripts/zenius_pack.sh 1293 # A20p
	bash scripts/zenius_pack.sh 1292 # A20
	bash scripts/zenius_pack.sh 1148 # A
	bash scripts/zenius_pack.sh 864 # 2014
	bash scripts/zenius_pack.sh 845 # 2013
	bash scripts/zenius_pack.sh 802 # X3
	bash scripts/zenius_pack.sh 546 # X2
	bash scripts/zenius_pack.sh 295 # X
	bash scripts/zenius_pack.sh 77 # SuperNOVA2
	bash scripts/zenius_pack.sh 1 # SuperNOVA
	bash scripts/zenius_pack.sh 41 # EXTREME
	bash scripts/zenius_pack.sh 31 # MAX2
	bash scripts/zenius_pack.sh 40 # MAX
	bash scripts/zenius_pack.sh 30 # 5
	bash scripts/zenius_pack.sh 39 # 4
	bash scripts/zenius_pack.sh 38 # 3
	bash scripts/zenius_pack.sh 32 # 2
	bash scripts/zenius_pack.sh 37 # 1

## LEGACY pipeline

# unzip data from ZiV zip files (error 9: .zip file not found)
unzip: strip
	for f in $(VERS); do \
		unzip -uo "$$f.zip" "*.sm" "*.ssc" "*.png" -d $$f || [ $$? -eq 9 ]; \
	done
	make fix

# perform various file fixes
fix:
	bash fix.sh 

# remove video/audio from ZiV zip files
strip:
	for f in $(VERS); do \
		zip -d "$$f.zip" "*.avi" "*.ogg" || [ $$? -eq 12 ]; \
	done

clean:
	mkdir -p log
	rm log/*.txt
