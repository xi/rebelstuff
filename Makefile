.PHONY: all
all:
	if [ ! -d .venv ]; then python3 -m venv .venv; fi
	.venv/bin/pip install django django-ical
	.venv/bin/python manage.py migrate
	.venv/bin/python manage.py compilemessages -l de
	.venv/bin/python manage.py loaddata sample_groups sample_data
	.venv/bin/python manage.py create_sample_users
	.venv/bin/python manage.py runserver
