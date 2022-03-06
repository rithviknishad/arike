#!/usr/bin/bash
git push heroku main;
heroku pg:reset DATABASE_URL -a rithviknishad-arike --confirm rithviknishad-arike;
heroku run python manage.py migrate;
cat fixtures.yaml | heroku run --no-tty -a rithviknishad-arike -- python manage.py loaddata --format=yaml -;