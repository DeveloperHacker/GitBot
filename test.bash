#!/usr/bin/env bash

DIR=$(dirname "$0")
PYTHONPATH="$DIR:$DIR/tests:$DIR/src"
export PYTHONPATH
python "$DIR/tests/run.py"