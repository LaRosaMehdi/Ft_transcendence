# # Start with a Python Alpine image as the base
# FROM python:3.9-alpine

# # Set the working directory in the container
# WORKDIR /usr/src/

# # Install Node.js and npm along with PostgreSQL client and other dependencies
# RUN apk add --no-cache postgresql-client libpq vim curl nodejs npm \
#     && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
#     # Install global npm packages
#     && npm install -g truffle \
#     && npm cache clean --force \
#     # Install Python packages
#     && pip install --upgrade pip \
#     # You can add psycopg2-binary to avoid compiling from source
#     && pip install psycopg2-binary \
#     # Cleanup
#     && apk del .build-deps \
#     && apk add --no-cache bash

# # Copy the Python dependencies file to the container
# COPY requirements.txt ./

# # Install the Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your application's code to the container
# COPY . .

# # Make sure the entrypoint script is executable
# RUN chmod +x /usr/src/entrypoint.sh

# # Expose the port the app runs on
# EXPOSE 443

# # Specify the command to run on container start
# CMD ["/usr/src/entrypoint.sh"]

FROM python:3.9

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        vim \
        curl \
        gnupg2 \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g truffle \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/

RUN pip install --upgrade pip  
RUN pip install channels
RUN pip install django-bootstrap-toolkit
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2
RUN pip install requests
RUN pip install djangorestframework
RUN pip install djangorestframework-simplejwt

COPY . .

EXPOSE 443

RUN chmod +777 /usr/src/entrypoint.sh

CMD ["/usr/src/entrypoint.sh"]