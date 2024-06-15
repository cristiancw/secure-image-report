LOCAL=`env | grep ^PWD= | cut -d '=' -f 2`
VERSION=3.12

.PHONY: help init build install clean clean-all

help: ##Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

init: clean-all ##Install the python virtual env and env dependencies to run this project.
	python${VERSION} -m venv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools wheel
	.venv/bin/pip install -U -r requirements.txt
	.venv/bin/python --version

build: clean ##Create the binary.
	.venv/bin/python setup.py sdist

install: build ##Create the binary.
	.venv/bin/pip install .
	cp .venv/bin/secure-image-report dist/

clean: ##Remove previous files and build artifacts.
	rm -fr build/
	rm -fr dist/
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name '*.egg-info' | xargs rm -rf
	find .venv/* -name '*secure-image-report*' | xargs rm -rf

clean-all: clean ##Remove previous files, build artifacts and .venv folder.
	rm -fr .venv/
