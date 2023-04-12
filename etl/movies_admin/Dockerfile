FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'
WORKDIR /movies_admin
COPY . .
RUN  pip install --upgrade pip && pip install -r requirements.txt
RUN python manage.py collectstatic --no-input
EXPOSE 8000
ENTRYPOINT uwsgi --ini uwsgi.ini