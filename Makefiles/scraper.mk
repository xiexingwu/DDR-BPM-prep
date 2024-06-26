
full_scrape: scrape_packs unzip scrape_songs dedupe fix 

scrape_packs:
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 1709 WORLD
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 1509 A3
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 1293 "A20 PLUS"
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 1292 A20
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 1148 A
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 864 2014
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 845 2013
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 802 X3
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 546 X2
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 295 X
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 77 SuperNOVA2
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 1 SuperNOVA
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 41 EXTREME
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 31 MAX2
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 40 MAX
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 30 5th
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 39 4th
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 38 3rd
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 32 2nd
	bash $(PROJ_DIR)/scripts/scrape/zenius_pack.sh 37 1st

# Some songs aren't located in the above packs.
# Download them into one of the folders
scrape_songs:
	bash $(PROJ_DIR)/scripts/scrape/zenius_song.sh 7568 2nd # PARANOiA KCET ~clean mix~
	bash $(PROJ_DIR)/scripts/scrape/zenius_song.sh 38006 3rd # LOVE THIS FEELIN'

# Some songs are duplicates
# Delete one version
dedupe:
	bash $(PROJ_DIR)/scripts/scrape/dedupe_song.sh "DYNAMITE RAVE" 3rd
	bash $(PROJ_DIR)/scripts/scrape/dedupe_song.sh "DYNAMITE RAVE (AIR Special)" SuperNOVA2
	bash $(PROJ_DIR)/scripts/scrape/dedupe_song.sh Happy X
	bash $(PROJ_DIR)/scripts/scrape/dedupe_song.sh "ever snow" MAX2
	bash $(PROJ_DIR)/scripts/scrape/dedupe_song.sh "La Bamba" EXTREME

unzip:
	bash $(PROJ_DIR)/scripts/scrape/unzip_pack.sh

# perform various file fixes
fix:
	bash $(PROJ_DIR)/scripts/scrape/fix.sh 

