FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /var/www
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
COPY . /var/www
VOLUME /var/www
EXPOSE 8000
CMD python manage.py collectstatic --noinput
CMD python manage.py runserver 0.0.0.0:8000