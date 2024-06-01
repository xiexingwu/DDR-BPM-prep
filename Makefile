SHELL := /bin/zsh

export PROJ_DIR=$(CURDIR)
include Makefiles/parser.mk
include Makefiles/scraper.mk
include Makefiles/deploy.mk

################################################################################
# CLEAN
################################################################################
clean:
	rm -fv log/*.txt || [ $$? -eq 1 ]

clobber: clean
	rm -fv data/**/*.zip
