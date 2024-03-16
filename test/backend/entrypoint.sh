#!/bin/bash

until pg_isready -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432 -q; do
  echo "Waiting for the database service to become available..."
  sleep 1
done

pip install web3

python -m pip install Pillow

python /usr/src/manage.py makemigrations
python /usr/src/manage.py migrate

#psql -U mehdi -d ft_transcendence_database -h ft_transcendence_database -p 5432

# if ! python /usr/src/manage.py shell -c "from users.models import User; print(User.objects.filter(is_superuser=True).exists())"; then
#     echo "Creating superuser..."
#     python /usr/src/manage.py shell <<EOF
# from django.contrib.auth import get_user_model
# User = get_user_model()
# User.objects.create_superuser('root', 'root@student.42nice.fr', 'toor')
# EOF
#     echo "Superuser created successfully."
# fi

exec python manage.py runserver 0.0.0.0:443
