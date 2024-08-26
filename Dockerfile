FROM python:3.12.5

WORKDIR /app

RUN git clone https://github.com/CHARLIEEDOKPA/task-django.git


WORKDIR /app/task-django

RUN git pull


RUN pip install -r requirements.txt





