open: setup
	nix-shell --run 'pycharm .'

test: setup
	nix-shell --run 'venv/bin/pytest'

bdist: test
	rm -rf dist
	venv/bin/python setup.py bdist_wheel

upload: bdist
	venv/bin/twine upload dist/*

setup: venv
	nix-shell --run 'venv/bin/pip install pip==23.3.1'
	nix-shell --run 'venv/bin/pip install -e .[dev]'

venv:
	nix-shell --run 'python3.7 -m venv venv'

.PHONY: setup test bdist
