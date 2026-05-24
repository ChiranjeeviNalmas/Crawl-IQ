.PHONY: venv install install-browsers run clean pull push help

BRANCH := feature/scrapper
PYTHON := python3
VENV   := .venv
PIP    := $(VENV)/bin/pip
VENV_PYTHON := $(VENV)/bin/python

# Load .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

help:
	@echo "Available commands:"
	@echo "  make venv             Create virtual environment (.venv)"
	@echo "  make install          Install Python dependencies into venv"
	@echo "  make install-browsers Install Playwright Chromium browser"
	@echo "  make run              Run default scraper (ai-engineer)"
	@echo "  make run-ai-engineer  Run a specific scraper by name"
	@echo "  make clean            Delete output folder"
	@echo "  make pull             Pull latest from $(BRANCH)"
	@echo "  make push msg='...'   Commit and push to $(BRANCH)"

venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Activate with: source $(VENV)/bin/activate"

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-browsers: install
	$(VENV_PYTHON) -m playwright install chromium

run:
	$(VENV_PYTHON) main.py

run-%:
	$(VENV_PYTHON) main.py $*

clean:
	rm -rf output/

pull:
	git pull origin $(BRANCH)

push:
	git add .
	git commit -m "$(msg)"
	git push origin $(BRANCH)
