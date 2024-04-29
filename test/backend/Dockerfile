FROM python:3.9-alpine

WORKDIR /usr/src/

RUN apk add --no-cache postgresql-client libpq vim curl nodejs npm \
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && npm install -g truffle \
    && npm cache clean --force \
    && pip install --upgrade pip \
    && pip install psycopg2-binary \
    && apk del .build-deps \
    && apk add --no-cache bash

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /usr/src/entrypoint.sh

EXPOSE 443

CMD ["/usr/src/entrypoint.sh"]

# FROM python:3.9
# 
# RUN apt-get update \
    # && apt-get install -y --no-install-recommends \
        # postgresql-client \
        # vim \
        # curl \
        # gnupg2 \
    # && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    # && apt-get install -y nodejs \
    # && npm install -g truffle \
    # && rm -rf /var/lib/apt/lists/*
# 
# WORKDIR /usr/src/
# 
# RUN pip install --upgrade pip  
# RUN pip install channels
# RUN pip install django-bootstrap-toolkit
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install psycopg2
# RUN pip install requests
# RUN pip install djangorestframework
# RUN pip install djangorestframework-simplejwt
# 
# COPY . .
# 
# EXPOSE 443
# 
# RUN chmod +777 /usr/src/entrypoint.sh
# 
# CMD ["/usr/src/entrypoint.sh"]