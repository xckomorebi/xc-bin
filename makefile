dest=$$HOME/bin

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
src := $(dir $(mkfile_path))

.PHONY: install

install:
	@ln -s $(src) $(dest)