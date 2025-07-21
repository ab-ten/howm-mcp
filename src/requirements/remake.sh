#!/bin/bash

cd "$(cd "$(dirname "$0")" && pwd)"

pip-compile -q --newline=lf --no-annotate --no-strip-extras \
            -o requirements-dev.txt requirements.in requirements-dev.in
pip-compile -q --newline=lf --no-annotate --no-strip-extras \
            -o requirements.txt requirements.in -c requirements-dev.txt
