# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /edeal
COPY requirements.txt /edeal/
RUN pip install -r requirements.txt
COPY . /edeal/