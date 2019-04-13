SHELL=/bin/bash

test:
	py.test -v --cov --cov-report term-missing # --doctest-modules

black:
	black -l 79 .

style:
	pycodestyle .

check: black style test

env-create:
	conda env create -f environment.yml

env-remove:
	conda env remove -n nxviz

docs:
	make -f docs/Makefile html

release:
	rm dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
