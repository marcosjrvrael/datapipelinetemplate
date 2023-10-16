SHELL := /bin/bash
ROOT_DIR:=$(shell pwd)

help: ## Show this helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

clean: ## Clean compiled and cache files.
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . | grep -E "__pycache__|.pyc|.pytest_cache|.DS_Store$$" | xargs rm -rf


create-requirements: ##Create requirments files to use in docker.
	poetry export -f requirements.txt --output requirements.txt --without-hashes

stylecheck: ## check for pep 8 formating errors.
	flake8 source/ \
			--builtins 'dbutils, sc, spark' \
			--per-file-ignores '__init__.py:F401' \
			--max-complexity 10 \
			--max-line-length 150

typecheck: ## check for pep 484 typehints errors.
	mypy source/ \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--ignore-missing-imports \
		--warn-unused-configs \
		--disable-error-code name-defined		

doccheck: ## check for pep 257 Docstrings errors, in Google format.
	pydocstyle source/ --convention google

##static-tests: Run all static tests.
static-tests: stylecheck typecheck doccheck

##docker-build: Call also clean environment temp files and run docker build.
docker-build:: clean create-requirements
	docker build \
		-f Dockerfile . -t apimagic

##docker-run: Run docker image if already builded or call docker-build before run it.
docker-run:: docker-build 
	docker run -it -v $(ROOT_DIR)/data:/source/data/:rw apimagic bash
