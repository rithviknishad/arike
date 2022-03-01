#!/usr/bin/bash
./manage.py migrate;
./manage.py loaddata fixtures/State.json;
./manage.py loaddata fixtures/District.json;
./manage.py loaddata fixtures/LsgBody.json;
./manage.py loaddata fixtures/Ward.json;
./manage.py loaddata fixtures/Facility.json;
./manage.py loaddata fixtures/User.json;