#!/bin/bash
cd example_project
eval PYTHONPATH=.. python manage.py test app
r=$?
cd ..
exit $r