FROM python:3.10
WORKDIR /movies_admin
COPY . .
RUN  pip install --upgrade pip && pip install -r requirements.txt
CMD [ "python", "main.py" ]