#!/bin/bash

pip install poetry
poetry config virtualenvs.create true

echo "Installing dependencies"
poetry install

echo "Installing Playwright browsers"
poetry run playwright install chromium

poetry run pre-commit install
# poetry shell
