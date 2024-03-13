#!/bin/bash

# Wait for the database service to become available
until pg_isready -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432 -q; do
  echo "Waiting for the database service to become available..."
  sleep 1
done

# Generate random numbers and fill a vector (example)
# Insert your code here
#Echo creating app_folder

#blockchain start
#cd blockchain_etherum && truffle compile
#truffle migrate --network development
#cd ..
pip install web3

#blockchain end


#psql -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432
# Start the Django development server or any other necessary commands
#python /usr/src/app/app/manage.py createsuperuser
#echo "APRES CREATE USER"
#echo "APRES start api"
#python -m pip install Pillow
#echo "APRES install pillow"
pip install requests

python /usr/src/manage.py makemigrations
python /usr/src/manage.py migrate
#echo "APRES migrate"
#python ./app/manage.py collectstatic --no-input
#echo "APRES STATIC"

# Check if the superuser exists, and if not, create it
if [ -z "$(python /usr/src/manage.py shell -c 'from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())')" ]; then
    echo "Creating superuser..."
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python /usr/src/manage.py shell
fi

exec python manage.py runserver 0.0.0.0:443
#echo "APRES run server"
