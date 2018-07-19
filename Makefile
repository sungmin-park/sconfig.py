test: setup
	venv/bin/pytest

setup: venv
	venv/bin/pip install pip==10.0.1
	venv/bin/pip install -e .[dev]

venv:
	python3.6 -m venv venv

.PHONY: setup
