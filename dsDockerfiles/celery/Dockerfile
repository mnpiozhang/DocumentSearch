FROM python:2.7-slim

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user

RUN pip install redis

ENV CELERY_VERSION 4.0.1
ENV DJANGO_VERSION 1.8.14

RUN pip install celery=="$CELERY_VERSION" django=="$DJANGO_VERSION" python-docx=="0.8.6" pdfminer elasticsearch

USER user
