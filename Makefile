SHELL := /bin/zsh
VERS = "DDR A3" "DDR A20 PLUS" "DDR A20" "DDR A" "DDR 2014" "DDR 2013" "DDR X3" "DDR X2" "DDR X" "DDR SuperNOVA2" "DDR SuperNOVA" "DDR EXTREME" "DDR MAX2" "DDR MAX" "DDR 5th" "DDR 4th" "DDR 3rd" "DDR 2nd" "DDR"

main:
	mkdir -p Resources/jackets
	python3 parse_courses.py
	python3 parse_simfiles.py

# load data.json to inspect data
load:
	python3 -i parse_simfiles.py -l

# remove video/audio from ZiV zip files
strip:
	for f in $(VERS); do \
		zip -d $$f.zip "*.avi" "*.ogg"; \
	done

# unzip data from ZiV zip files
unzip:
	for f in $(VERS); do \
		unzip -u $$f.zip "*.sm" "*.ssc" "*.png" -d $$f; \
	done

# check for duplicates, missing songs, etc.
check_songs:
	python check_songs.py
