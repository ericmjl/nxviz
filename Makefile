test:
	py.test --cov --cov-report term-missing -v

env-create:
	conda env create -f environment.yml

env-remove:
	source deactivate
	conda env remove -n nxviz

docs:
	cd docs
	make html

env-recreate: env-remove env-create
