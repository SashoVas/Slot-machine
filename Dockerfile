FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-venv python3-dev build-essential
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY Server ./Server

EXPOSE 8000

CMD ["python3","Server/manage.py","runserver","0.0.0.0:8000"]