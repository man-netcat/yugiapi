FROM python:3.11-slim-buster

WORKDIR /app

ENV FLASK_APP=yugiapi.py 
ENV FLASK_RUN_HOST=0.0.0.0 

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "yugiapi.py"]
