@echo off
START "" http://127.0.0.1:8000/
call python manage.py runserver
