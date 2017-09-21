SHELL=/bin/bash

test:
	py.test --cov --cov-report term-missing -v --doctest-modules

env-create:
	conda env create -f environment.yml

env-remove:
	conda env remove -n nxviz

docs:
	make -f docs/Makefile html
