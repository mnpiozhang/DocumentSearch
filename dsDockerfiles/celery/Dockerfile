FROM python:2.7-slim

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user

RUN pip install redis

ENV CELERY_VERSION 4.0.1

RUN pip install celery=="$CELERY_VERSION"

USER user
CMD ["celery", "-A","DocumentSearch","worker"]