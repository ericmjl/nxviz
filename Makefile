.PHONY: docs

SHELL=/bin/bash

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
	mkdocs build

release:
	rm dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
