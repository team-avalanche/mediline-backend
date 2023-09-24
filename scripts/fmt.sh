#!/bin/sh
echo "Make sure your project virtual environment is activated for correct results!"
python -m black .
python -m isort .
python -m ruff .