FROM python:3.12.5

WORKDIR /app

RUN git clone https://github.com/CHARLIEEDOKPA/task-django


WORKDIR /app/task-django


ENV DJANGO_DEBUG=True

RUN git pull


RUN pip install -r requirements.txt





