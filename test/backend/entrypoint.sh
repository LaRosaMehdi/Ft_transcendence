#!/bin/bash

until pg_isready -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432 -q; do
  echo "Waiting for the database service to become available..."
  sleep 1
done

cd blockchain_etherum
truffle migrate --network development
cd ..
pip install django-sslserver
pip install web3

python -m pip install Pillow

# python manage.py flush 
python /usr/src/manage.py makemigrations
python /usr/src/manage.py migrate

if ! python /usr/src/manage.py shell -c "from users.models import User; exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"; then
    # Ici je cree le super User
    python /usr/src/manage.py createsuperuser --no-input --username root 
    if [ $? -eq 0 ]; then
        echo "Superuser created successfully."
        # Ici je set le mdp
        python /usr/src/manage.py shell -c "from users.models import User; superuser = User.objects.get(username='root'); superuser.set_password('toor'); superuser.save()"
        echo "Superuser password set successfully."
    else
        echo "Failed to create superuser."
    fi
else
    echo "Superuser already exists."
fi


exec python /usr/src/manage.py runsslserver --certificate /usr/src/ssl/cert.pem --key /usr/src/ssl/key.pem 0.0.0.0:443
