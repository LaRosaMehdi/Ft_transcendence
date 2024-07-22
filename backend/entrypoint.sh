#!/bin/bash

crond


until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -q; do
  echo "Waiting for the database service to become available..."
  sleep 1
done

cd blockchain_etherum
truffle migrate --network development
cd ..
pip install django-sslserver
pip install web3
pip install django-environ
python -m pip install Pillow

python /usr/src/manage.py makemigrations
python /usr/src/manage.py migrate

if ! python /usr/src/manage.py shell -c "from users.models import User; exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"; then
    python /usr/src/manage.py createsuperuser --no-input --username "$DJANGO_ADMIN_USER"
    if [ $? -eq 0 ]; then
        echo "Superuser created successfully."
        python /usr/src/manage.py shell -c "from users.models import User; superuser = User.objects.get(username='"$DJANGO_ADMIN_USER"'); superuser.set_password('"$DJANGO_ADMIN_PASSWORD"'); superuser.save()"
        echo "Superuser password set successfully."
    else
        echo "Failed to create superuser."
    fi
else
    echo "Superuser already exists."
fi


exec python /usr/src/manage.py runsslserver --certificate /usr/src/ssl/cert.pem --key /usr/src/ssl/key.pem 0.0.0.0:443
