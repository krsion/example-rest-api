#!/usr/bin/env bash
SILENT=true
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
export FLASK_ENV=development
flask run