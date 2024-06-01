SHELL := /bin/zsh

include Makefiles/parser.mk
include Makefiles/scraper.mk

# Don't accientally overwrite main
main:
	make -f Makefiles/parser.mk main

################################################################################
# CLEAN
################################################################################
clean:
	rm -fv log/*.txt || [ $$? -eq 1 ]

clobber: clean
	rm -fv data/**/*.zip
