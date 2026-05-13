.PHONY: install run dev venv build check publish publish-test

PYTHON := .venv/bin/python

venv:
	python3 -m venv .venv

install:
	$(PYTHON) -m pip install -e .

run:
	mango

dev:
	XDG_CONFIG_HOME=.test-config mango

build:
	$(PYTHON) -m pip install --quiet build
	rm -rf dist build
	$(PYTHON) -m build

check:
	$(PYTHON) -m twine check dist/*

publish-test:
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish:
	$(PYTHON) -m twine upload dist/*
