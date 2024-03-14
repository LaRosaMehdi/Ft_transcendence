FROM python:3

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
RUN pip install django-bootstrap-toolkit
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2
RUN pip install requests
COPY . .

EXPOSE 443

# Add entrypoint script to wait for database availability
#COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +777 /usr/src/entrypoint.sh

# Run the entrypoint script instead of directly starting the Django server
CMD ["/usr/src/entrypoint.sh"]
