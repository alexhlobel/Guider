venv:
	pip install virtualenv
	virtualenv -p /usr/bin/python3.9 venv
	source venv/bin/activate

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

deploy:
	docker-compose build
	docker-compose up -d

heroku:
	git push heroku main
