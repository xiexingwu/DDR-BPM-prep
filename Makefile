SHELL := /bin/zsh

export PROJ_DIR=$(CURDIR)
export SRC_DIR=$(CURDIR)/src
export SEED_DIR=$(CURDIR)/data
export BUILD_DIR=$(PROJ_DIR)/build
include Makefiles/scraper.mk
include Makefiles/parser.mk
include Makefiles/deploy.mk

# Run after scraping (parse & downscale jackets)
main: clobber parse predeploy

release:
	bash $(PROJ_DIR)/scripts/deploy/release.sh
################################################################################
# CLEAN
################################################################################
clean:
	rm -fv log/*.txt || [ $$? -eq 1 ]

clobber: clean
	rm -fv data/**/*.zip || [ $$? -eq 1 ]
	rm -fv build/**/*.json || [ $$? -eq 1 ]
