.PHONY: install run dev venv

venv:
	python3 -m venv .venv

install:
	pip install -e .

run:
	mango

dev:
	XDG_CONFIG_HOME=.test-config mango
