#!/usr/bin/bash
git push heroku main;
heroku pg:reset DATABASE_URL -a rithviknishad-arike --confirm rithviknishad-arike;
heroku run python manage.py migrate;
cat fixtures/State.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;
cat fixtures/District.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;
cat fixtures/LsgBody.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;
cat fixtures/Ward.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;
cat fixtures/Facility.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;
cat fixtures/User.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;
cat fixtures/Patient.json | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=json -;