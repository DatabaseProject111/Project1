#!/bin/sh
export PATHONPATH=`pwd`
python3 -m coverage run --timid --branch --source fe,be --concurrency=thread -m pytest -v --ignore=fe/data
python3 -m coverage combine
python3 -m coverage report
python3 -m coverage html
