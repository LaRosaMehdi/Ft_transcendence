# Generated by Django 3.2.10 on 2024-06-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20240610_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='level',
            field=models.CharField(choices=[('pool', 'Pool'), ('quarter_final', 'Quarter Final'), ('semi_final', 'Semi Final'), ('final', 'Final'), ('final', 'Final'), ('none', 'None')], default='none', max_length=20),
        ),
    ]