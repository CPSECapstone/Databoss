#!/bin/bash

# Script to run all tests with coverage.py

cd ${0%/*}
coverage run -m unittest discover -s tests/