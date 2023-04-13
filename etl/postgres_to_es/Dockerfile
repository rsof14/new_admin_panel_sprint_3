FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/app
COPY . .
RUN  pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 9200
CMD [ "python", "main.py" ]