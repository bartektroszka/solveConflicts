#!/bin/bash

set -e
cd "$(dirname "$0")"

export FLASK_APP=__init__.py
export FLASK_ENV=development
flask run