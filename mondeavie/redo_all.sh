#!/bin/bash
python manage.py dumpdata admin_activities --natural --indent=4 1> old_app.json
cp db.sqlite3 db.sqlite3.old
rm db.sqlite3
./drop_migration.sh
cd ..
find -name "*.pyc" -exec rm -rf {} \;
cd mondeavie/
./manage.py makemigrations
./manage.py syncdb
./manage.py loaddata old_app.json
