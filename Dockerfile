FROM python:3.10-alpine
USER root
COPY requirements.txt .
RUN pip install -r requirements.txt