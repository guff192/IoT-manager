#! /usr/bin/env bash

set -e  # Exit immediately if a command exits with a non-zero status.
set -x  # Print commands and their arguments as they are executed.

python app/tests_pre_start.py  # Ensure database is running

bash scripts/test.sh "$@"  # Run tests
