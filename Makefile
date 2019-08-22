.PHONY: all
all:
	if [ ! -d .venv ]; then python3 -m venv .venv; fi
	.venv/bin/pip install django
	.venv/bin/python manage.py migrate
	.venv/bin/python manage.py runserver
