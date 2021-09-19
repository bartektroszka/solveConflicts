#!/bin/bash

set -e
cd "$(dirname "$0")"

export FLASK_APP=__init__.py
flask run