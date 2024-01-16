# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /yugiapi

ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
