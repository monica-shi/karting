#!/bin/bash
python3 manage.py migrate && python3 manage.py collectstatic && gunicorn --workers 1 karting.wsgi