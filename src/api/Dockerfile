FROM tiangolo/uvicorn-gunicorn:python3.10

ENV PYTHONUNBUFFERED True

RUN apt update && apt install -y make

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
