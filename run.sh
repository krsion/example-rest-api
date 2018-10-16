#!/usr/bin/env bash
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export FLASK_ENV=development
flask run