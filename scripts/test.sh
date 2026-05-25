#! /usr/bin/env bash

set -e  # Exit immediately if a command exits with a non-zero status.
set -x  # Print commands and their arguments as they are executed.

source venv/bin/activate
python -m coverage run -m pytest tests/
python -m coverage report
