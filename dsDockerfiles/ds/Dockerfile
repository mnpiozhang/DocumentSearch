FROM python:2.7-slim

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		#maybe occur error
		#postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV DJANGO_VERSION 1.8.14

WORKDIR /usr/src/app
EXPOSE 8000

RUN pip install mysqlclient psycopg2 django=="$DJANGO_VERSION"  python-docx=="0.8.6" celery=="4.0.1"  pdfminer elasticsearch redis

ENV TZ Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["python", "manage.py","runserver","0.0.0.0:8000"]