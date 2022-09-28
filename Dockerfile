FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 0 main:server
