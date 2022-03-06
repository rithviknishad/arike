#!/usr/bin/bash
./manage.py migrate;
./manage.py loaddata fixtures.yaml --format=yaml