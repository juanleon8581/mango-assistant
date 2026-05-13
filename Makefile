.PHONY: install run dev venv build check publish publish-test

venv:
	python3 -m venv .venv

install:
	pip install -e .

run:
	mango

dev:
	XDG_CONFIG_HOME=.test-config mango

build:
	rm -rf dist build
	python -m build

check:
	twine check dist/*

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*
