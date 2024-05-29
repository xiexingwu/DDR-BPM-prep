SHELL := /bin/zsh
VERS = "DDR A3" "DDR A20 PLUS" "DDR A20" "DDR A" "DDR 2014" "DDR 2013" "DDR X3" "DDR X2" "DDR X" "DDR SuperNOVA2" "DDR SuperNOVA" "DDR EXTREME" "DDR MAX2" "DDR MAX" "DDR 5th" "DDR 4th" "DDR 3rd" "DDR 2nd" "DDR"

main: check_songs
	$(info ###### CONSIDER RUNNING: make load; AND CHECKING THE VARIABLE: data)
	python3 src/parse_courses.py
	python3 src/parse_simfiles.py

# check for duplicates, missing songs, etc.
check_songs:
	$(info ###### MAKE SURE all_songs.txt HAS ENDING NEW LINE)
	$(info ###### MAKE SURE YOU HAVE RUN THE FOLLOWING: make unzip)
	python src/check_songs.py

# unzip data from ZiV zip files (error 9: .zip file not found)
unzip: strip
	for f in $(VERS); do \
		unzip -uo "$$f.zip" "*.sm" "*.ssc" "*.png" -d $$f || [ $$? -eq 9 ]; \
	done
	make fix

# load data.json to inspect data
load:
	python3 -i src/parse_simfiles.py -l

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
