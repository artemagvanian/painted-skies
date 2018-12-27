#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python3 manage.py migrate
python3 manage.py collectstatic --noinput --verbosity 0
gunicorn paintedskies.wsgi -w 4 --worker-class gevent -b 0.0.0.0:8000 --chdir=/app
