LOCAL=`env | grep ^PWD= | cut -d '=' -f 2`
VERSION=3.12

.PHONY: help init build install clean clean-all

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

init: clean-all ## Install the python virtual env and env dependencies to run this project.
	python${VERSION} -m venv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools wheel pyinstaller autopep8 pip-check
	.venv/bin/pip install -U -r requirements.txt
	.venv/bin/python --version

type-check: ## Run mypy to check type annotations.
	.venv/bin/mypy src/

build: clean ## Create the binary.
	.venv/bin/python setup.py sdist

install: build ## Create the binary.
#	.venv/bin/pip install .
#	zip -j dist/secure-image-report.zip .venv/bin/secure-image-report
	.venv/bin/pyinstaller --name secure-image-report --onefile --paths=src/ src/com/cristiancw/secure_image_report/secure_image_report.py
	zip -j dist/secure-image-report.zip dist/secure-image-report

clean: ## Remove previous files and build artifacts.
	rm -fr build/
	rm -fr dist/
	rm -fr *.spec
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name '*.egg-info' | xargs rm -rf
	find .venv/* -name '*secure-image-report*' | xargs rm -rf

clean-all: clean ## Remove previous files, build artifacts and .venv folder.
	rm -fr .venv/
