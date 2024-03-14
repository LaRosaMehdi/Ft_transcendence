#!/bin/bash

# Wait until Postgres is ready
until pg_isready -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432 -q; do
  echo "Waiting for the database service to become available..."
  sleep 1
done



#blockchain start
#cd blockchain_etherum && truffle compile
#truffle migrate --network development
#cd ..
pip install web3

#blockchain end


#psql -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432
#pour les images
python -m pip install Pillow
#echo "APRES install pillow"


python /usr/src/manage.py makemigrations
python /usr/src/manage.py migrate
#echo "APRES migrate"


if ! python /usr/src/manage.py shell -c "from django.contrib.auth.models import User; exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"; then
    # Ici je cree le super User
    python /usr/src/manage.py createsuperuser --no-input --username root --email test@gmail.com
    if [ $? -eq 0 ]; then
        echo "Superuser created successfully."
        # Ici je set le mdp
        python /usr/src/manage.py shell -c "from django.contrib.auth.models import User; superuser = User.objects.get(username='root'); superuser.set_password('toor'); superuser.save()"
        echo "Superuser password set successfully."
    else
        echo "Failed to create superuser."
    fi
else
    echo "Superuser already exists."
fi

exec python manage.py runserver 0.0.0.0:443
