test: setup
	venv/bin/pytest

bdist: test
	rm -rf dist
	venv/bin/python setup.py bdist_wheel

upload: bdist
	venv/bin/twine upload dist/*

setup: venv
	venv/bin/pip install pip==19.3.1
	venv/bin/pip install -e .[dev]

venv:
	python3.7 -m venv venv

.PHONY: setup test bdist
