FROM python:3.9.9

WORKDIR /usr/src/api/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/api/

RUN pip install -r requirements.txt

COPY . /usr/src/api/
