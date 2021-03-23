VENV_PATH := .venv/main

.venv:
	python3.8 -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/pip install -r requirements.in

requirements.txt: requirements.in .venv
	$(VENV_PATH)/bin/pip freeze > requirements.txt

.PHONY: black
black:
	black -l 100 ppa_api tests examples

.PHONY: flake8
flake8:
	flake8 --ignore W503,E501,W293 ppa_api tests examples

.PHONY: pytest
pytest:
	$(VENV_PATH)/bin/pip uninstall -y ppa-api
	$(VENV_PATH)/bin/pip install -e ".[test]"
	$(VENV_PATH)/bin/pytest tests/ --cov-report term --cov=ppa_api
	$(VENV_PATH)/bin/coverage html
