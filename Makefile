VENV_PATH := .venv/main
PYTHON := $(VENV_PATH)/bin/python3.10

.venv:
	python3.10 -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/pip install -r requirements.in

.PHONY: pip-deps
pip-deps: requirements.in .venv
	$(VENV_PATH)/bin/pip install pip==21.3.1 setuptools==58.3.0 wheel==0.37.0
	$(VENV_PATH)/bin/pip install -r requirements.in

.PHONY: black
black:
	black -l 100 ppa_api tests examples

.PHONY: flake8
flake8:
	flake8 --ignore W503,E501,W293 ppa_api tests examples

.PHONY: build
build:
	$(PYTHON) setup.py bdist_wheel

.PHONY: pytest
pytest:
	$(VENV_PATH)/bin/pip uninstall -y ppa-api
	$(VENV_PATH)/bin/pip install -e ".[test]"
	$(VENV_PATH)/bin/pytest tests/ --cov-report term --cov=ppa_api
	$(VENV_PATH)/bin/coverage html
