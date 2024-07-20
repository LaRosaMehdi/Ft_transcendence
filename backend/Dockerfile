FROM python:3.9-alpine

WORKDIR /usr/src/

RUN apk add --no-cache postgresql-client libpq vim curl nodejs npm dcron \
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && npm install -g truffle \
    && npm cache clean --force \
    && pip install --upgrade pip \
    && pip install psycopg2-binary \
    && apk del .build-deps \
    && apk add --no-cache bash

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install typing_extensions --upgrade
RUN pip install django-cron

COPY . .

RUN chmod +x /usr/src/entrypoint.sh

RUN touch /var/log/cron_output.log
RUN chmod 644 /var/log/cron_output.log
COPY crontab /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron
RUN crontab /etc/cron.d/mycron

EXPOSE 8080

CMD ["/usr/src/entrypoint.sh"]