parse: check_songs songs courses
	$(info ################################################################################)
	$(info # Once finished, run `make load` to inspect the variable `songs`)
	$(info ################################################################################)

songs:
	poetry run python $(SRC_DIR)/parse_simfiles.py

courses:
	poetry run python $(SRC_DIR)/parse_courses.py

# check for duplicates, missing songs, etc.
check_songs: fix clean
	$(info ################################################################################)
	$(info # 1. Make sure all_songs.txt has ending new line)
	$(info # 2. Make sure you ran a full scrape: make full_scrape)
	$(info ################################################################################)
	poetry run python $(SRC_DIR)/check_songs.py

# load data & write
write:
	poetry run python $(SRC_DIR)/parse_simfiles.py -l -w

# load data to inspect
load:
	poetry run python $(SRC_DIR)/parse_simfiles.py -l -i

# perform various file fixes
fix:
	bash $(PROJ_DIR)/scripts/parse/fix.sh 
