# Generated by Django 3.2.25 on 2024-07-18 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='twofactor_enabled',
            field=models.BooleanField(default=False),
        ),
    ]