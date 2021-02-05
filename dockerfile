FROM python:3.8
WORKDIR /app
ADD requirements.txt /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 8000
ENTRYPOINT python manage.py makemigrations
ENTRYPOINT python manage.py migrate & python manage.py migrate & python manage.py collectstatic --noinput & gunicorn meta.wsgi --bind :8000

