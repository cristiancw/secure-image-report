LOCAL=`env | grep ^PWD= | cut -d '=' -f 2`
VERSION=3.12

.PHONY: help init build install clean clean-all

help: ##Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

init: ##Install the python virtual env and env dependencies to run this project.
	$(MAKE) clean-all
	python${VERSION} -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -U -r requirements.txt
	.venv/bin/python --version

build: ##Create the binary.
	$(MAKE) clean
	.venv/bin/python setup.py develop

install: ##Create the binary.
	.venv/bin/pyinstaller --name secure-image-report --onefile  src/__main__.py
	zip -j dist/secure-image-report.zip dist/secure-image-report 

clean: ##Remove previous files and build artifacts.
	rm -fr build/
	rm -fr dist/
	rm -fr secure-image-report.spec
	rm -fr ./src/*.egg-info/
	find .venv/* -name '*secure-image-report*' | xargs rm -rf
	find ./src/ -type d -name '__pycache__' | xargs rm -rf

clean-all: ##Remove previous files, build artifacts and .venv folder.
	$(MAKE) clean
	rm -fr .venv/
