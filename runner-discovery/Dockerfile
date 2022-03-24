FROM python:3.7

SHELL ["/bin/bash", "-c"]

WORKDIR /opt/project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./* ./
